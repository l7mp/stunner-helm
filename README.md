# STUNner Helm charts

## Table of Contents

- [Important](#important)
- [Deploying](#deploying)
    - [With the Gateway Operator](#with-the-stunner-gateway-operator)
    - [Standalone mode](#without-the-operator-in-standalone-mode)
- [Features](#features)
    - [Resources](#resources)
    - [UDP multithreading](#udp-multithreading)
    - [Graceful shutdown](#graceful-shutdown)
    - [Monitoring](#monitoring)

## Important
There are a few things to know before jumping right into using STUNner
- STUNner must installed into the same namespace as the `gatewayclass` and config was in case you are using STUNner with the gateway-operator

## Deploying
There are two ways to install and use STUNner. It is advised to use STUNner with the STUNner Gateway Operator.

### With the STUNner Gateway Operator

```console
helm repo add stunner https://l7mp.io/stunner
helm repo update

helm install stunner-gateway-operator stunner/stunner-gateway-operator --create-namespace --namespace=<your-namespace>

helm install stunner stunner/stunner --create-namespace --namespace=<your-namespace>
```

### Without the Operator in Standalone Mode 

```console
helm repo add stunner https://l7mp.io/stunner
helm repo update

helm install stunner stunner/stunner --set stunner.standalone.enabled=true --create-namespace --namespace=<your-namespace> 
```

## Features

In the following part the currently available features will be introduced. How to activate, access, configure and use them.

Currently, the list is:
- [Resources](#resources)
- [UDP multithreading](#udp-multithreading)
- [Graceful shutdown](#graceful-shutdown)
- [Monitoring](#monitoring)

### Resources

When running applications in a Kubernetes cluster it is essential to manage their [resource usage](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/). Carefully configuring them enables the user to have control of the number of replicas and prevent resource starvation.
The [default](/helm/stunner/values.yaml) resource request in the chart and limit is the following:
```yaml
resources:
  limits:
    cpu: 2
    memory: 512Mi
  requests:
    cpu: 500m
    memory: 128Mi
```
Meaning every started `stunner` pod will request `0.5 CPU` core and `128 mebibytes` of memory. These pods will only start in case the cluster can successfully allocate the given amount of resources. If the cluster lacks of resources it is advised to lower the requested value. This is not the only reason why the user should carefully configure the resources.

About the resource limits, in order to not stress the Kubernetes scheduler it is advised to keep the limits down and scale out (increase) the number of running pods if needed. Actually, it is the way, do not be afraid to scale in Kubernetes. To learn more about the scaling process take a look at our full [scaling guide](/README_SCALING.md).

### UDP multithreading

Multi-threaded UDP listeners adds the ability for STUNner to run UDP listeners over multiple parallel readloops. The
idea is to create a configurable number of UDP server sockets using `SO_REUSEPORT` and spawn a
separate goroutine to run a parallel readloop for each. The kernel will load-balance allocations
across the sockets/readloops per the IP 5-tuple, so the same allocation will always stay at the
same CPU. This allows UDP listeners to scale to multiple CPUs.

Note that this is enabled only for UDP at the moment: TCP, TLS and DTLS listeners spawn a
per-client readloop anyway. Also note that `SO_REUSEPORT` is not portable, so currently we enable
this only for UNIX architectures.

The feature is exposed via the command line flag `--udp-thread-num=<THREAD_NUMBER>` in
`stunnerd`. In the Helm chart it can be enabled or disabled with the `--set stunner.deployment.container.stunnerd.udpMultithreading.enabled=true` flag. By default it is enabled with 16 separate readloops each UDP listener.
```yaml
udpMultithreading:
  enabled: true
  readLoopsPerUDPListener: 16
```

### Graceful shutdown

STUNner has full support for graceful shutdown in Kubernetes. This means that `stunner` pods will remain alive as long as there are active allocations via the embedded TURN server, and a pod will automatically remove itself once all allocations through it are deleted or timed out. 

Note that the default TURN refresh lifetime is 10 minutes so STUNner may remain alive well after the last client goes away. This occurs when an UDP allocation is left open by a client (spontaneous UDP client-side connection closure cannot be reliably detected by the server). In such cases, after 10 mins the allocation will timeout and get deleted, which will then let `stunnerd` to terminate. 
This feature enables the full support for graceful scale-down: the user can scale the number of `stunner` instances up and down as they wish and no harm should be made to active client connections meanwhile. 
Caveats: 
- currently the max lifetime for `stunner` to remain alive after deleted in 1 hour: this means that `stunner` will remain active only for 1 hour after it has been deleted/scaled-down. You can always set this in by adjusting the `terminationGracePeriod` on your `stunnerd` pods.
- if there are active (or very recent) TURN allocations then the `stunner` pod may refuse to be removed after a kubectl delete. Use `kubectl delete pod --grace-period=0 --force -n stunner stunner-XXX` to force removal.

The default termination period is set to 3600 seconds (1 hour). To modify it use the `--set stunner.deployment.container.terminationGracePeriodSeconds=<NEW_PERIOD_IN_SECONDS>` flag.

### Monitoring

The monitoring guide assumes an up-and-running `Stunner-Gateway-Operator` in the user's Kubernetes cluster.

#### Configuration

Metrics collection is *not* enabled in the default installation. In order to open the
metrics-collection endpoint for a [gateway hierarchy](https://github.com/l7mp/stunner/blob/main/doc/GATEWAY.md), configure an
appropriate HTTP URL in the `metricsEndpoint` field of corresponding the
[GatewayConfig](https://github.com/l7mp/stunner/blob/main/doc/GATEWAY.md#gatewayconfig) resource.

For instance, the below GatewayConfig will expose the metrics-collection server on the URL
`http://:8080/metrics` in all the STUNner media gateway instances of the current gateway hierarchy.

```yaml
apiVersion: stunner.l7mp.io/v1alpha1
kind: GatewayConfig
metadata:
  name: stunner-gatewayconfig
  namespace: stunner
spec:
  userName: "my-user"
  password: "my-password"
  metricsEndpoint: "http://:8080/metrics"
```

#### Installation

A full-fledged Prometheus+Grafana helm chart is available in the repo [here](/helm/stunner-prometheus/). To use this chart, the installation steps involve enabling monitoring in STUNner, and installing the Prometheus+Grafana stack with helm.

1. **Configure STUNner to expose the metrics**

- Deploy STUNner with monitoring enabled to enable the monitoring port of STUNner pods
```console
helm install stunner stunner/stunner --create-namespace --namespace=stunner --set stunner.deployment.monitoring.enabled=true
```

- [Expose the STUNner metrics-collection server in the GatewayConfig](#configuration)

2. **Install the Prometheus+Grafana stack with a helm chart**

This helm chart creates a ready-to-use Prometheus+Grafana stack in the `monitoring` namespace: installs Prometheus along with the prometheus-operator, and Grafana; configures PodMonitor for monitoring STUNner pods, and sets up Prometheus as a datasource for Grafana.

```console
helm repo add stunner https://l7mp.io/stunner
helm repo update

helm install prometheus stunner/stunner-prometheus
```

Learn more about how to enable, configure and use monitoring [here](https://github.com/l7mp/stunner/blob/main/doc/MONITORING.md#installation).


## Help

STUNner development is coordinated in Discord, feel free to [join](https://discord.gg/DyPgEsbwzc).

## License

MIT License - see [LICENSE](LICENSE) for full text.