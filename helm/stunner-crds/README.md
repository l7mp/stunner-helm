# STUNner CRDs

A dedicated Helm chart for managing the lifecycle of STUNner Custom Resource Definitions (CRDs) and optionally installing the official Kubernetes Gateway API CRDs.

## Why a separate chart?

Helm does **not** upgrade resources placed in the `crds/` directory during `helm upgrade`. By moving CRDs into a regular Helm template (via this sub-chart), `helm upgrade` will correctly update the CRD schemas when new fields are added.

This chart is consumed as a dependency by the main [`stunner-gateway-operator`](../stunner-gateway-operator) chart, but can also be installed standalone.

## Included CRDs

### STUNner CRDs (always installed)

| CRD | Group | Scope |
| --- | --- | --- |
| `GatewayConfig` | `stunner.l7mp.io` | Namespaced |
| `StaticService` | `stunner.l7mp.io` | Namespaced |
| `Dataplane` | `stunner.l7mp.io` | Cluster |
| `UDPRoute` | `stunner.l7mp.io` | Namespaced |

### Gateway API CRDs (optional)

This chart can optionally install the official Kubernetes Gateway API CRDs via the [Envoy Gateway `gateway-crds-helm`](https://gateway.envoyproxy.io/docs/install/gateway-crds-helm-api/) chart.

| Resource | API Group |
|----------|-----------|
| `GatewayClass` | `gateway.networking.k8s.io` |
| `Gateway` | `gateway.networking.k8s.io` |
| `HTTPRoute` | `gateway.networking.k8s.io` |
| `GRPCRoute` | `gateway.networking.k8s.io` |
| `TCPRoute` | `gateway.networking.k8s.io` |
| `UDPRoute` | `gateway.networking.k8s.io` |
| `TLSRoute` | `gateway.networking.k8s.io` |
| `ReferenceGrant` | `gateway.networking.k8s.io` |

## Install

### Standalone (default: STUNner + Gateway API CRDs)

By default, the standalone chart installs both STUNner and Gateway API CRDs:

```console
helm install stunner-crds stunner/stunner-crds
```

If your cluster already provides Gateway API (e.g. GKE), disable them:

```console
helm install stunner-crds stunner/stunner-crds \
    --set gatewayCrds.enabled=false
```

### As a dependency of the operator

By default, the `stunner-gateway-operator` chart installs STUNner CRDs but **not** Gateway API CRDs (since many users run on managed clusters that already provide them):

```console
helm install stunner-gateway-operator stunner/stunner-gateway-operator --create-namespace \
    --namespace=stunner-system
```

If you also need Gateway API CRDs (e.g. not on GKE):

```console
helm install stunner-gateway-operator stunner/stunner-gateway-operator --create-namespace \
    --namespace=stunner-system \
    --set stunnerCrds.gatewayCrds.enabled=false
```

If you already have the CRDs installed and want to skip the dependency entirely:

```console
helm install stunner-gateway-operator stunner/stunner-gateway-operator --create-namespace \
    --namespace=stunner-system \
    --set stunnerCrds.enabled=false
```

## Configuration

| Name | Description | Default (standalone) |
|------|-------------|----------------------|
| `gatewayCrds.enabled` | Install official Gateway API CRDs via Envoy Gateway chart | `true` |
| `gatewayCrds.crds.gatewayAPI.channel` | Gateway API channel: `standard` or `experimental` | `experimental` |

## Upgrading CRDs

Because these CRDs are rendered as regular templates (not in the special `crds/` folder), a standard `helm upgrade` will patch the CRD definitions:

```console
helm upgrade stunner-crds stunner/stunner-crds
```

Or, if installed via the operator chart:

```console
helm upgrade stunner-gateway-operator stunner/stunner-gateway-operator
```

## Uninstalling

**Warning:** Uninstalling this chart will remove the CRDs and **all** custom resources (e.g. all your `GatewayConfig`, `UDPRoute`, etc. objects) from the cluster. Only uninstall if you are sure you want to destroy all STUNner configuration.

```console
helm uninstall stunner-crds
```
