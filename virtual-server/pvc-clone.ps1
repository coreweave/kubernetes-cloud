Param
    (
        [Parameter(ValueFromPipeline,Mandatory=$true,HelpMessage='Name of Virtual Server or PVC to clone from')]
        [ValidateNotNullOrEmpty()]
        [string]
        $Source,
        [Parameter(ValueFromPipeline,Mandatory=$true,HelpMessage='Desired name of destination PVC')]
        [ValidateNotNullOrEmpty()]
        [string]
        $Target,
        [Parameter(ValueFromPipeline,Mandatory=$false,HelpMessage='Destination reigon, if different from source')]
        [ValidateSet('EWR1','ORD1','LAS1')]
        [string]
        $TargetReigon
    )

Function Invoke-ActionPrompt
    {
        Param
            (
                [string]
                $Text
            )
       
        do
            {
                try
                    {
                        $Prompt = Read-Host -Prompt $Text -EA Stop
                        if(!($Prompt -contains 'yes' -or $Prompt -contains 'no' -or $Prompt -contains 'y' -or $Prompt -contains 'n')){throw{}}
                    }
                catch{Write-Host "`nMust use 'yes' or 'no'`n" -ForegroundColor Red}
            }
        until($Prompt -ne $NULL -and ($Prompt -contains 'yes' -or $Prompt -contains 'no' -or $Prompt -contains 'y' -or $Prompt -contains 'n'))
    
        if($Prompt.StartsWith('y')){Return [bool]$true}
        Elseif($Prompt.StartsWith('n')){Return [bool]$false}
    }


try{@('kubectl','virtctl')|%{get-command $_ -ErrorAction Stop | out-null}}
catch
    {
        Write-Warning "Required binaries not detected" -WarningAction Continue
        Write-Warning "Please follow instructions at https://docs.coreweave.com/coreweave-kubernetes/getting-started#install-kubernetes-command-line-tools" -WarningAction Continue
        Return 1
    }

if(kubectl get vmi $($source) --ignore-not-found=true)
    {
        $SourcePVC = kubectl get vmi $($source) -o 'jsonpath={".spec.volumes[?(@.name==''dv'')].persistentVolumeClaim.claimName"}'
        
        switch(Invoke-ActionPrompt -Text "Found running VM instance $($source).`nStop it? [y/N]")
            {
                $true
                    {
                        virtctl stop $($source)
                        $NotifyString = "Waiting for $($source) to stop..." 
                        Write-Host $NotifyString -ForegroundColor Cyan -BackgroundColor Black
                        while(kubectl get vmi $($source) --ignore-not-found=true)
                            {
                                $NotifyString += "."
                                Write-Host $NotifyString -ForegroundColor Cyan -BackgroundColor Black
                                Start-Sleep -Seconds 2
                            }
                        $NotifyString += "Stopped"
                        Write-Host $NotifyString -ForegroundColor Cyan -BackgroundColor Black
                    }
                $false
                    {
                        Write-Warning "Cannot clone PVC of a running VM"
                        Return 1
                    }
            }
    }

Elseif(kubectl get pvc $($source) --ignore-not-found=true){$SourcePVC = $Source}

Else
    {
        Write-Warning "Did not find PVC or VM instance $($Source)"
        Return 1
    }

$SourcePVCCLass = kubectl get pvc $($SourcePVC) -o 'jsonpath={".spec.storageClassName"}'
$SourcePVCSize = kubectl get pvc $($SourcePVC) -o 'jsonpath={".spec.resources.requests.storage"}'
$Reigon = $SourcePVCCLass.split('-') | select -Last 1
if($Reigon -eq 'replica'){$Reigon = 'ord1'}

$DestinationPVC = $($Target)+'-'+$(Get-Date -Format yyyyMMdd)+'-block-'+$($Reigon)

if($TargetReigon -and !($TargetReigon -eq $Reigon))
    {
        $Namespace = kubectl config view --minify --output 'jsonpath={..namespace}'
        $DestinationPVCClass = ($SourcePVCCLass -replace $Reigon,$TargetReigon).ToLower()
        $DestinationPVC = ($DestinationPVC -replace $Reigon,$TargetReigon).ToLower()
@"
apiVersion: cdi.kubevirt.io/v1beta1
kind: DataVolume
metadata:
  annotations:
  labels:
  name: $($DestinationPVC)
  namespace: $($Namespace)
spec:
  pvc:
    accessModes:
    - ReadWriteOnce
    resources:
      requests:
        storage: $($SourcePVCSize)
    storageClassName: $($DestinationPVCClass)
    volumeMode: Block
  source:
    pvc:
      name: $($SourcePVC)
      namespace: $($Namespace)
"@ | kubectl apply -f -

        $NotifyString = "Waiting for DV $($DestinationPVC) to complete clone..."
        Write-Host $NotifyString -ForegroundColor Cyan -BackgroundColor Black
        while(!((kubectl get dv $($DestinationPVC) --ignore-not-found=true --output 'jsonpath={.status.phase}') -eq 'Succeeded'))
            {
                $NotifyString = "Waiting for DV $($DestinationPVC) to complete clone..." + $(kubectl get dv $($DestinationPVC) --ignore-not-found=true --output 'jsonpath={.status.progress}')
                Write-Host $NotifyString -ForegroundColor Cyan -BackgroundColor Black
                Start-Sleep -Seconds 10
            }
        $NotifyString += 'done.'
        Write-Host $NotifyString -ForegroundColor Cyan -BackgroundColor Black
    }

Else
    {
@"
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: $($DestinationPVC)
spec:
  accessModes:
  - ReadWriteOnce
  storageClassName: $($SourcePVCCLass)
  volumeMode: Block
  resources:
    requests:
      storage: $($SourcePVCSize)
  dataSource:
    kind: PersistentVolumeClaim
    name: $($SourcePVC)
"@ | kubectl apply -f -

        $NotifyString = "Waiting for $($DestinationPVC) to be bound..."
        Write-Host $NotifyString -ForegroundColor Cyan -BackgroundColor Black
        while(!((kubectl get pvc $($DestinationPVC) --ignore-not-found=true -o 'jsonpath={".status.phase"}') -eq 'Bound'))
            {
                $NotifyString += "."
                Write-Host $NotifyString -ForegroundColor Cyan -BackgroundColor Black
                Start-Sleep -Seconds 1
            }
        $NotifyString += 'done.'
        Write-Host $NotifyString -ForegroundColor Cyan -BackgroundColor Black
    }

if(kubectl get pvc $($DestinationPVC) --ignore-not-found=true){Write-Host "Clone of $($SourcePVC) to $($DestinationPVC) is complete`nSource VM instance $($Source) can be started up or destroyed" -ForegroundColor Cyan -BackgroundColor Black}
