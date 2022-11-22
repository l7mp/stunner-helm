# Prometheus and Grafana for monitoring STUNner instances

## Installation

From the helm repo:
```console
helm install prometheus stunner/stunner-prometheus
```

Using local files:
```console
helm install prometheus .
```

The helm chart creates the namespace `monitoring` and install Prometheus along with the prometheus-operator, and Grafana.

## Acknowledgments

Helm chart is based on the [l7mp-prometheus chart](https://github.com/l7mp/l7mp/tree/master/helm-charts/l7mp-prometheus).
