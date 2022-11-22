# Prometheus and Grafana for monitoring STUNner instances

## Prerequisites

Deploy STUNner with monitoring enabled:
```console
helm install stunner ./stunner --create-namespace --namespace=stunner --set stunner.deployment.monitoring.enabled=true
```
Enable the STUNner metrics endpoint:
```console
kubectl -n stunner patch gatewayconfigs.stunner.l7mp.io stunner-gatewayconfig --patch '{"spec": {"metricsEndpoint": "http://0.0.0.0:8080/metrics" }}' --type=merge
```

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

## Acknowledgments

Helm chart is based on the [l7mp-prometheus chart](https://github.com/l7mp/l7mp/tree/master/helm-charts/l7mp-prometheus).
