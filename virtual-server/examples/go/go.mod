module github.com/coreweave/kubernetes-cloud/virtual-server/examples/go

go 1.13

replace (
	github.com/go-kit/kit => github.com/go-kit/kit v0.3.0
	github.com/openshift/api => github.com/openshift/api v0.0.0-20210105115604-44119421ec6b
	github.com/openshift/client-go => github.com/openshift/client-go v0.0.0-20210112165513-ebc401615f47
	github.com/operator-framework/operator-lifecycle-manager => github.com/operator-framework/operator-lifecycle-manager v0.17.0
	github.com/operator-framework/operator-registry => github.com/operator-framework/operator-registry v1.16.1
	k8s.io/api => k8s.io/api v0.20.2
	k8s.io/apimachinery => k8s.io/apimachinery v0.20.2
	k8s.io/client-go => k8s.io/client-go v0.20.2
	k8s.io/cluster-bootstrap => k8s.io/cluster-bootstrap v0.16.4
	kubevirt.io/containerized-data-importer => kubevirt.io/containerized-data-importer v1.26.1
	sigs.k8s.io/structured-merge-diff => sigs.k8s.io/structured-merge-diff v1.0.1-0.20191108220359-b1b620dd3f06
)

require (
	github.com/coreweave/virtual-server v1.15.0
	github.com/spf13/pflag v1.0.5
	k8s.io/api v0.20.2
	k8s.io/apimachinery v0.20.2
	kubevirt.io/client-go v0.39.0
	sigs.k8s.io/controller-runtime v0.8.3
)
