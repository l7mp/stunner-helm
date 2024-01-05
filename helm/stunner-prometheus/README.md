# Prometheus and Grafana for monitoring STUNner instances

## Prerequisites

Install stunner-gateway-operator with Prometheus support:

```console
helm install stunner-gateway-operator stunner/stunner-gateway-operator --create-namespace --namespace=stunner-system --set stunnerGatewayOperator.dataplane.spec.enableMetricsEndpoint=true
```

Alternatively, you can enable it on existing installations by setting `enableMetricsEndpoint: true` in your [Dataplane](GATEWAY.md#dataplane) objects.

> [!NOTE]
> Metrics are exposed at `http://:8080/metrics` on each STUNner pod

## Installation

From the helm repo:
```console
helm install prometheus stunner/stunner-prometheus
```

Using local files:
```console
helm install prometheus .
```

The helm chart creates the namespace `monitoring` and installs Prometheus along with the prometheus-operator, and Grafana.

> [!NOTE]
> You can also install node-exporter by adding `--set nodeExporter.create=true` to the install command.

## Help

STUNner development is coordinated in Discord, feel free to [join](https://discord.gg/DyPgEsbwzc).

## Acknowledgments

Helm chart is based on the [l7mp-prometheus chart](https://github.com/l7mp/l7mp/tree/master/helm-charts/l7mp-prometheus).
