# CRD Management in STUNner

This document explains how Custom Resource Definitions (CRDs) are handled in the STUNner Helm charts and provides guidance for different cluster setups.

## Background

STUNner requires two sets of CRDs to function:

1. **Kubernetes Gateway API CRDs** (`gateway.networking.k8s.io`)
   - Provided by the upstream [Kubernetes Gateway API](https://gateway-api.sigs.k8s.io/) project.
   - Some managed Kubernetes offerings (like **GKE**) already include these.
   - Other clusters need to install them manually, or can let the STUNner CRD chart install them.

2. **STUNner CRDs** (`stunner.l7mp.io`)
   - Custom resources specific to STUNner: `GatewayConfig`, `Dataplane`, `StaticService`, `UDPRoute`.
   - Owned and versioned by the STUNner project.

### The problem with Helm's `crds/` directory

Helm has a special `crds/` directory for bundling CRDs, but it comes with a critical limitation: **CRDs in `crds/` are only installed on `helm install`, never upgraded on `helm upgrade`.** This means that if STUNner adds a new field to `GatewayConfig` in a future release, users who run `helm upgrade` will **not** receive the updated schema, leading to validation errors.

To solve this, we moved the STUNner CRDs out of the `crds/` folder and into a dedicated sub-chart (`helm/stunner-crds`) that is consumed as a regular Helm dependency. Because the CRDs are now rendered as normal templates, `helm upgrade` will patch them correctly.

---

## Current Architecture

```
helm/
├── stunner-crds/                  # Standalone CRD chart
│   ├── templates/stunner-crds.yaml
│   ├── Chart.yaml  (optionally depends on gateway-crds-helm)
    │   └── values.yaml (gatewayCrds.enabled toggle)
└── stunner-gateway-operator/      # Main operator chart
    ├── Chart.yaml  (depends on stunner-crds as stunnerCrds)
    ├── values.yaml (stunnerCrds.enabled toggle)
    └── templates/
```

### What changed?

- **Gateway API CRDs are no longer bundled** in the operator chart. Instead, the `stunner-crds` chart can optionally pull them in via the [Envoy Gateway `gateway-crds-helm`](https://gateway.envoyproxy.io/docs/install/gateway-crds-helm-api/) chart.
- **STUNner CRDs live in `helm/stunner-crds`.** The operator chart pulls them in as a conditional dependency.
- **`helm upgrade` now updates STUNner CRDs.** No more stale schemas.
- **You have three independent knobs:**
  1. Install STUNner CRDs or not (`stunnerCrds.enabled`)
  2. Install Gateway API CRDs or not (`stunnerCrds.gatewayCrds.enabled`)
  3. Choose the Gateway API channel (`stunnerCrds.gatewayCrds.crds.gatewayAPI.channel`)

---

## Quick Start

### 1. Decide whether you need Gateway API CRDs

| Platform | Action |
|----------|--------|
| **GKE** | Gateway API is built-in. No need to install CRDs. |
| **EKS / AKS / Self-managed** | Either install them manually or let STUNner install them (see below). |
| **Already installed** | Skip this step. |

> Note: The default is the **Experimental** channel of the Gateway API because STUNner uses `TCPRoute` and `UDPRoute`, which are not yet in the standard channel. The exact version may vary per STUNner release; check the [STUNner compatibility guide](https://github.com/l7mp/stunner#supported-versions) for details.

### 2. Install STUNner (default: with both CRD sets)

The default installation includes both STUNner and Gateway API CRDs:

```console
helm repo add stunner https://l7mp.io/stunner
helm install stunner-gateway-operator stunner/stunner-gateway-operator \
    --create-namespace --namespace=stunner-system
```

### 3. Install STUNner (skip Gateway API CRDs)

For GKE and clusters that already have Gateway API:

```console
helm repo add stunner https://l7mp.io/stunner
helm install stunner-gateway-operator stunner/stunner-gateway-operator \
    --create-namespace --namespace=stunner-system \
    --set stunnerCrds.gatewayCrds.enabled=false
```

### 4. Install STUNner (skip all CRDs)

If you manage both CRD sets yourself (e.g. via GitOps):

```console
helm install stunner-gateway-operator stunner/stunner-gateway-operator \
    --create-namespace --namespace=stunner-system \
    --set stunnerCrds.enabled=false
```

---

## Common Scenarios

### Scenario A: Fresh cluster, no Gateway API

```console
# Install STUNner with both STUNner and Gateway API CRDs (default)
helm install stunner-gateway-operator stunner/stunner-gateway-operator \
    --create-namespace --namespace=stunner-system
```

### Scenario B: GKE cluster with Gateway API enabled

```console
# GKE already has Gateway API CRDs.
# Skip the bundled Gateway API CRDs to avoid conflicts.
helm install stunner-gateway-operator stunner/stunner-gateway-operator \
    --create-namespace --namespace=stunner-system \
    --set stunnerCrds.gatewayCrds.enabled=false
```

### Scenario C: GitOps workflow (Flux / Argo CD)

If you manage CRDs via GitOps, you likely want full control over when CRDs are applied.

```console
# In your GitOps repo, install the standalone CRD chart first:
helm install stunner-crds stunner/stunner-crds

# Then install the operator with CRD dependency disabled:
helm install stunner-gateway-operator stunner/stunner-gateway-operator \
    --namespace=stunner-system \
    --set stunnerCrds.enabled=false
```

This prevents the operator chart from trying to manage the CRDs and avoids conflicts with your GitOps reconciler.

### Scenario D: Upgrading an existing STUNner installation

```console
helm upgrade stunner-gateway-operator stunner/stunner-gateway-operator \
    --namespace=stunner-system
```

Because CRDs are now part of a regular sub-chart, `helm upgrade` will update the schemas automatically.

---

## Installing from source

If you are installing directly from this Git repository (instead of the Helm repo), you must build the chart dependencies first:

```console
git clone https://github.com/l7mp/stunner-helm.git
cd stunner-helm
helm dependency build helm/stunner-crds
helm dependency build helm/stunner-gateway-operator
helm install stunner-gateway-operator ./helm/stunner-gateway-operator \
    --create-namespace --namespace=stunner-system
```

---

## Community Gateway API Helm charts

The Kubernetes Gateway API project itself does **not** publish an official Helm chart for CRDs. They distribute raw YAML manifests via GitHub Releases.

We now optionally integrate the [Envoy Gateway `gateway-crds-helm`](https://gateway.envoyproxy.io/docs/install/gateway-crds-helm-api/) chart, which is a well-maintained Helm chart that packages the official Gateway API CRDs (plus optional Envoy Gateway-specific CRDs). This gives you a Helm-native way to install and manage the Gateway API CRDs.

If you prefer not to use the Envoy Gateway chart, you can still install Gateway API CRDs manually:

```console
kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.3.0/standard-install.yaml
```

Other community-maintained options on [Artifact Hub](https://artifacthub.io) also exist:

| Chart | Repository | Notes |
|-------|------------|-------|
| `gateway-api-crds` | `wiremind/wiremind-helm-charts` | Experimental channel CRDs |
| `gateway-api-crds` | `portefaix/portefaix-hub` | Gateway API CRDs |
| `gateway-api-crds` | `deimosfr/deimosfr-charts` | Community maintained |

---

## FAQ

### Will uninstalling the operator delete my CRDs?

If you installed via the default path (CRDs as a dependency), running `helm uninstall stunner-gateway-operator` **will** also remove the `stunner-crds` release and therefore delete the CRDs and all your STUNner custom resources. If you want CRDs to survive the operator uninstall, install the `stunner-crds` chart separately with the `helm.sh/resource-policy: keep` annotation (not enabled by default).

### What happens if I forget to install Gateway API CRDs?

The STUNner operator pods will fail to start because the Kubernetes API server will not recognize `GatewayClass`, `Gateway`, and `HTTPRoute` resources. You will see errors in the operator logs.

### Can I use an older version of the Gateway API CRDs?

STUNner is tested against specific Gateway API versions. Using a significantly older or newer version may cause compatibility issues. Always consult the [STUNner release notes](https://github.com/l7mp/stunner/releases) for the recommended Gateway API version.

---

## References

- [Helm CRD Best Practices](https://helm.sh/docs/chart_best_practices/custom_resource_definitions/)
- [Kubernetes Gateway API Installation](https://gateway-api.sigs.k8s.io/guides/)
- [Envoy Gateway CRDs Helm Chart](https://gateway.envoyproxy.io/docs/install/gateway-crds-helm-api/)
- [STUNner Installation Docs](https://github.com/l7mp/stunner/blob/main/docs/INSTALL.md)
