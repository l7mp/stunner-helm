# CRD Management in STUNner

## Overview

STUNner requires two sets of CRDs to function:

1. **STUNner CRDs** (`stunner.l7mp.io`) — `GatewayConfig`, `Dataplane`, `StaticService`, `UDPRoute`
2. **Kubernetes Gateway API CRDs** (`gateway.networking.k8s.io`) — `GatewayClass`, `Gateway`, `HTTPRoute`, etc.

---

## Architecture

```
stunner-gateway-operator/
├── crds/
│   └── stunner-crds.yaml                        # STUNner CRDs (always installed)
├── charts/
│   ├── gateway-api-standard-crds/               # Standard channel subchart (toggleable)
│   │   └── crds/gateway-api-crds.yaml
│   └── gateway-api-experimental-crds/           # Experimental channel subchart (toggleable)
│       └── crds/gateway-api-crds.yaml
├── Chart.yaml
├── values.yaml
└── templates/
```

All CRDs are placed in Helm's `crds/` directory, which means:

- CRDs are installed **before** templates are rendered
- CRDs **survive** `helm uninstall`

---

## Configuration

| Value | Description | Default |
|-------|-------------|---------|
| `standardCrds.enabled` | Install Gateway API Standard channel CRDs | `true` |
| `experimentalCrds.enabled` | Install Gateway API Experimental channel CRDs | `false` |

STUNner CRDs are always installed and cannot be disabled.

---

## Installation

### Default (Standard channel)

```console
helm repo add stunner https://l7mp.io/stunner
helm install stunner-gateway-operator stunner/stunner-gateway-operator \
    --create-namespace --namespace=stunner-system
```

### Experimental channel

```console
helm install stunner-gateway-operator stunner/stunner-gateway-operator \
    --create-namespace --namespace=stunner-system \
    --set standardCrds.enabled=false \
    --set experimentalCrds.enabled=true
```

### Skip Gateway API CRDs

For clusters that already have Gateway API (e.g. GKE):

```console
helm install stunner-gateway-operator stunner/stunner-gateway-operator \
    --create-namespace --namespace=stunner-system \
    --set standardCrds.enabled=false
```

---

## Common Scenarios

### Fresh cluster, no Gateway API

```console
helm install stunner-gateway-operator stunner/stunner-gateway-operator \
    --create-namespace --namespace=stunner-system \
    --set standardCrds.enabled=false \
    --set experimentalCrds.enabled=true
```

### GKE cluster with Gateway API enabled

```console
helm install stunner-gateway-operator stunner/stunner-gateway-operator \
    --create-namespace --namespace=stunner-system \
    --set standardCrds.enabled=false
```

### GitOps workflow (Flux / Argo CD)

Install Gateway API CRDs manually, then install the operator without them:

```console
kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.4.1/experimental-install.yaml

helm install stunner-gateway-operator stunner/stunner-gateway-operator \
    --create-namespace --namespace=stunner-system \
    --set standardCrds.enabled=false
```

### Upgrading an existing installation

```console
helm upgrade stunner-gateway-operator stunner/stunner-gateway-operator \
    --namespace=stunner-system
```

> **Note:** STUNner CRDs in the `crds/` directory are not updated by `helm upgrade`. If a new release includes CRD schema changes, you must update them manually.

---

## Installing from source

```console
git clone https://github.com/l7mp/stunner-helm.git
cd stunner-helm
helm dependency build helm/stunner-gateway-operator
helm install stunner-gateway-operator ./helm/stunner-gateway-operator \
    --create-namespace --namespace=stunner-system
```

---

## FAQ

### Will uninstalling the operator delete my CRDs?

No. CRDs are placed in the `crds/` directory, so `helm uninstall` will **not** remove them. CRDs and all custom resources (e.g. `GatewayConfig`, `Dataplane`, etc.) will remain in the cluster after uninstall.

### What happens if I forget to install Gateway API CRDs?

The STUNner operator pods will fail to start because the Kubernetes API server will not recognize `GatewayClass`, `Gateway`, and `HTTPRoute` resources. You will see errors in the operator logs.

### Can I use a different version of the Gateway API CRDs?

STUNner is tested against specific Gateway API versions. The bundled version is v1.4.1. Using a significantly older or newer version may cause compatibility issues. Always consult the [STUNner release notes](https://github.com/l7mp/stunner/releases) for the recommended Gateway API version.

---

## References

- [Helm CRD Best Practices](https://helm.sh/docs/chart_best_practices/custom_resource_definitions/)
- [Kubernetes Gateway API Installation](https://gateway-api.sigs.k8s.io/guides/)
- [STUNner Installation Docs](https://github.com/l7mp/stunner/blob/main/docs/INSTALL.md)
