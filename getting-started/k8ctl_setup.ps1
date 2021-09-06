Param
    (
        [switch]
        $Silent,
        [switch]
        $Remove
    )

Start-Transcript -Path $env:TEMP\k8setup.log -IncludeInvocationHeader -Append

Function Install-k8sctl
    {
        Param
            (
                [switch]
                $Kubectl,
                [switch]
                $Virtctl,
                [switch]
                $IsAdmin
            )

        if(!(test-path $env:ProgramData\k8s -ErrorAction SilentlyContinue)){New-Item -Path $env:ProgramData -Name k8s -ItemType Directory -Force | out-null}
        $ProgressPreference = 'SilentlyContinue'

        if($Kubectl){Invoke-WebRequest -UseBasicParsing -Uri "https://dl.k8s.io/release/$(Invoke-RestMethod -Uri "https://dl.k8s.io/release/stable.txt")/bin/windows/amd64/kubectl.exe" -OutFile $env:ProgramData\k8s\kubectl.exe}

        if($Virtctl){Invoke-WebRequest -Uri $((Invoke-restmethod https://api.github.com/repos/kubevirt/kubevirt/releases/latest).assets.browser_download_url.Where({$_ -like '*virtctl-*-windows-amd64.exe'}))  -OutFile $env:ProgramData\k8s\virtctl.exe}

        $Path = (Get-ItemProperty -Path 'Registry::HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\Session Manager\Environment' -Name PATH).path
        if(!($Path.Contains($("$env:ProgramData\k8s"+';'))))
            {
                if(!($path.EndsWith(';'))){$Path += ';'}
                $path += $("$env:ProgramData\k8s"+';')
                if($IsAdmin){Set-ItemProperty -Path 'Registry::HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\Session Manager\Environment' -Name PATH -Value $Path}
                $env:path = $path
            }

        $Alias = @('New-Alias k kubectl','New-Alias virt virtctl')
        if((test-path $Profile -ErrorAction SilentlyContinue) -and !(gc $Profile -ErrorAction SilentlyContinue| select-string kubectl -ErrorAction SilentlyContinue)){Add-Content $Profile -Value $Alias}
        Else
            {
                if(!(test-path $($profile.trim($($profile.split('\') | select -Last 1))) -ErrorAction SilentlyContinue)){New-Item -ItemType Directory -Path $($profile.trim($($profile.split('\') | select -Last 1))) |out-null}
                Set-Content $Profile -Value $Alias
            }

    }

function Check-AdminContext
    {
        Param
            (
                [switch]
                $Elevate
            )
        
        [bool]$IsAdmin = [bool](([System.Security.Principal.WindowsIdentity]::GetCurrent()).groups -match "S-1-5-32-544")

        if(!($IsAdmin) -and $Elevate)
            {
                Write-Warning 'Current context is not administrative - attempting to elevate' -WarningAction Continue
                Start-Sleep -Seconds 2
                if(!($($MyInvocation.MyCommand.Path))){Write-Warning 'No invocation command, likely executed via call operator. Re-run as admin manually.' -WarningAction Continue}
                Else
                    {
                        $param = '-NoLogo', '-File', $MyInvocation.MyCommand.Path
                        if($PSBoundParameters.Count -ge 1){$param += $PSBoundParameters.GetEnumerator() |%{'-'+$_.Key+' '+"'"+$_.Value+"'"}}
                        Start-Process "powershell.exe" -ArgumentList $param -Verb 'RunAs'
                        exit $LASTEXITCODE
                    }
            }

        Elseif(!($IsAdmin)){Write-Warning -Message "Current context is not administrative" -WarningAction Continue}

        Return $IsAdmin
    }

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

if(!(test-path $env:ProgramData\k8s\kubectl.exe -ErrorAction SilentlyContinue) -or !(get-command kubectl -ErrorAction SilentlyContinue))
    {
        if($Silent){Install-k8sctl -Kubectl -IsAdmin}

        Else
            {        
                switch(Invoke-ActionPrompt -Text "kubectl not detected - would you like to install? Yes or No:")
                    {
                        $true
                            {
                                if(!(Check-AdminContext))
                                    {
                                        switch(Invoke-ActionPrompt -Text "We need to be an admin to update PATH. Elevate? Yes or No:")
                                            {
                                                $true
                                                    {
                                                        Check-AdminContext -Elevate
                                                    }
                                                $false
                                                    {
                                                        Install-k8sctl -Kubectl
                                                    }
                                            }
                                    }

                                Else{Install-k8sctl -Kubectl -IsAdmin}
                            }

                        $false
                            {
                               Write-Warning -Message "kubectl not installed - please download and add to PATH" -WarningAction Continue
                            }
                    }
            }
    }

if(!(test-path $env:ProgramData\k8s\virtctl.exe -ErrorAction SilentlyContinue) -or !(get-command virtctl -ErrorAction SilentlyContinue))
    {
        if($Silent){Install-k8sctl -Virtctl -IsAdmin}

        Else
            {
        
                switch(Invoke-ActionPrompt -Text "virtctl not detected - would you like to install? Yes or No:")
                    {
                        $true
                            {
                                if(!(Check-AdminContext))
                                    {
                                        switch(Invoke-ActionPrompt -Text "We need to be an admin to update PATH. Elevate? Yes or No:")
                                            {
                                                $true
                                                    {
                                                        Check-AdminContext -Elevate
                                                    }
                                                $false
                                                    {
                                                        Install-k8sctl -Virtctl
                                                    }
                                            }
                                    }

                                Else{Install-k8sctl -Virtctl -IsAdmin}
                            }

                        $false
                            {
                               Write-Warning -Message "virtctl not installed - please download and add to PATH" -WarningAction Continue
                            }
                    }
            }
    }

if(!(test-path $env:userprofile\.kube\config -ErrorAction SilentlyContinue))
    {
        if($Silent){Write-Warning "Kubeconfig not found, please copy to $env:userprofile\.kube\config" -WarningAction Continue}

        Else
            {        
                switch(Invoke-ActionPrompt -Text "Kubeconfig not found.`nWould you like to import a cw-kubeconfig file? Yes or No:")
                    {
                        $True
                            {
                                $Prompt = Read-Host -Prompt "Please drag your cw-kubeconfig file into the PowerShell Window, or type the path manually:"
                                $Prompt = $prompt.trim('"').Trim('''')

                                if(test-path $Prompt)
                                    {
                                        if(!(test-path $env:userprofile\.kube)){New-Item -ItemType Directory -Path $env:userprofile -Name .kube -Force | out-null}
                                        Copy-Item -Path $Prompt -Destination $env:userprofile\.kube\config -Force -Verbose
                                    }

                                Else{Write-Warning -Message "Could not parse path $($Prompt)" -WarningAction Continue}
                            }

                        $False{Write-Warning "Kubeconfig not found, please copy to $env:userprofile\.kube\config" -WarningAction Continue}
                    }
            }
    }

if($Remove)
    {
        Check-AdminContext -Elevate
        remove-item $env:ProgramData\k8s -Force -Recurse -Verbose
        remove-item $Prompt -Force -Verbose
        remove-item $env:userprofile\.kube\config -Force -Verbose
        $Path = (Get-ItemProperty -Path 'Registry::HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\Session Manager\Environment' -Name PATH).path
        if(($Path.Contains($("$env:ProgramData\k8s"+';'))))
            {
                $path.replace('C:\ProgramData\k8s;','')
                Set-ItemProperty -Path 'Registry::HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\Session Manager\Environment' -Name PATH -Value $Path
            }
    }

Stop-Transcript
