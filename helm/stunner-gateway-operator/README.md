# STUNner

The Helm chart of STUNner: A Kubernetes media gateway for WebRTC.

## Note

The official documentation for the STUNner installation methods is in the repository of STUNner. For further information, see the [documentation](https://github.com/l7mp/stunner/blob/main/docs/INSTALL.md).

## Installation

This chart is the recommended way to deploy the STUNner ecosystem into your cluster.

The command below installs the stable version of STUNner. In particular, it installs only the STUNner control plane (the gateway operator and the authentication service); the dataplane is automatically provisioned by the operator when needed (but see below). We recommend using the `stunner-system` namespace to keep the full STUNner control plane in a single scope.

```console
helm install stunner-gateway-operator stunner/stunner-gateway-operator --create-namespace \
    --namespace=stunner-system
```

And that's all: you don't need to install the dataplane separately, because this is handled automatically by the operator. The `stunnerd` pods created by the operator can be customized using the Dataplane custom resource: you can specify the `stunnerd` container image version, provision resources per `stunnerd` pod, deploy into the host network namespace, and more; see the documentation [here](https://pkg.go.dev/github.com/l7mp/stunner-gateway-operator/api/v1#DataplaneSpec).

## CRD Management

This chart installs CRDs from two sources:

- STUNner CRDs are bundled in the chart `crds/` folder and installed by Helm.
- Gateway API CRDs are installed via chart dependencies controlled by values.

### Gateway API CRDs

By default, the operator chart installs the official Kubernetes Gateway API CRDs from the standard channel (`standardCrds.enabled=true`).

- **GKE / Managed clusters:** If your cluster already provides Gateway API, you may want to skip the bundled Gateway API CRDs to avoid conflicts:
  ```console
  helm install stunner-gateway-operator stunner/stunner-gateway-operator --create-namespace \
      --namespace=stunner-system \
      --set standardCrds.enabled=false
  ```
- **Self-managed clusters:** The default install is all you need.

#### Install Gateway API CRDs manually (explicit control)

If you prefer to manage Gateway API CRDs yourself:

```console
kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.3.0/standard-install.yaml
helm install stunner-gateway-operator stunner/stunner-gateway-operator --create-namespace \
    --namespace=stunner-system \
    --set standardCrds.enabled=false
```

> Note: The exact version required may vary with STUNner releases; consult the [STUNner compatibility matrix](https://github.com/l7mp/stunner#supported-versions) for the recommended Gateway API version.

To install Gateway API experimental CRDs as well:

```console
helm install stunner-gateway-operator stunner/stunner-gateway-operator --create-namespace \
    --namespace=stunner-system \
    --set experimentalCrds.enabled=true
```

To upgrade an existing installation (which will also upgrade the CRDs if needed):

```console
helm upgrade stunner-gateway-operator stunner/stunner-gateway-operator --namespace=stunner-system
```

## Parameters

### CRD options

| Name                        | Description                                                                | Value   |
| --------------------------- | -------------------------------------------------------------------------- | ------- |
| `standardCrds.enabled`      | If true, install Gateway API CRDs from the standard channel dependency.   | `true`  |
| `experimentalCrds.enabled`  | If true, install Gateway API CRDs from the experimental channel dependency. | `false` |

### Logging

| Name                        | Description                                                            | Value  |
| --------------------------- | ---------------------------------------------------------------------- | ------ |
| `logging.operator.format`   | Log format for the gateway operator. Must be `text` or `json`.        | `text` |
| `logging.operator.level`    | Log level for the gateway operator zap logger (pass-through string).  | `info` |
| `logging.dataplane.format`  | Log format for managed dataplane pods. Must be `text` or `json`.      | `text` |
| `logging.authService.format` | Log format for the auth service. Must be `text` or `json`.           | `text` |

### STUNner Gateway operator

| Name                                                                            | Description                                                      | Value                                     |
| ------------------------------------------------------------------------------- | ---------------------------------------------------------------- | ----------------------------------------- |
| `stunnerGatewayOperator.enabled`                                                | If true, deploy the operator.                                    | `true`                                    |
| `stunnerGatewayOperator.deployment.name`                                        | Name of the deployment for the operator.                         | `stunner-gateway-operator`                |
| `stunnerGatewayOperator.deployment.podLabels`                                   | Labels for the deployment pods.                                  | `{}`                                      |
| `stunnerGatewayOperator.deployment.affinity`                                    | Affinity settings for the deployed operator instance.            | `{}`                                      |
| `stunnerGatewayOperator.deployment.tolerations`                                 | Tolerations for pod assignment.                                  | `[]`                                      |
| `stunnerGatewayOperator.deployment.replicas`                                    | Number of replicas of the operator to be deployed.               | `1`                                       |
| `stunnerGatewayOperator.deployment.nodeSelector`                                | Node labels for pod assignment.                                  | `{kubernetes.io/os: linux}`               |
| `stunnerGatewayOperator.deployment.imagePullSecrets`                            | Image pull secrets for the image.                                | `[]`                                      |
| `stunnerGatewayOperator.deployment.topologySpreadConstraints`                   | Constraints to control how pods are spread across the cluster.   | `[]`                                      |
| `stunnerGatewayOperator.deployment.container`                                   | Container configuration values.                                  |                                           |
| `stunnerGatewayOperator.deployment.container.manager`                           | Configuration values for the STUNner Gateway Operator container. |                                           |
| `stunnerGatewayOperator.deployment.container.manager.image.name`                | The name of the image to use.                                    | `docker.io/l7mp/stunner-gateway-operator` |
| `stunnerGatewayOperator.deployment.container.manager.image.pullPolicy`          | The pull policy for the image.                                   | `IfNotPresent`                            |
| `stunnerGatewayOperator.deployment.container.manager.image.tag`                 | The tag for the image.                                           | `1.1.1`                                   |
| `stunnerGatewayOperator.deployment.container.manager.resources.limits.cpu`      | CPU limits for the container.                                    | `1000m`                                   |
| `stunnerGatewayOperator.deployment.container.manager.resources.limits.memory`   | Memory limits for the container.                                 | `512Mi`                                   |
| `stunnerGatewayOperator.deployment.container.manager.resources.requests.cpu`    | CPU requests for the container.                                  | `250m`                                    |
| `stunnerGatewayOperator.deployment.container.manager.resources.requests.memory` | Memory requests for the container.                               | `128Mi`                                   |
| `stunnerGatewayOperator.deployment.container.manager.args`                      | Arguments for the container.                                     | `[--health-probe-bind-address=:8081, --metrics-bind-address=127.0.0.1:8080, --leader-elect]` |

### Dataplane

Default dataplane configuration for the operator to use. See more [here](https://github.com/l7mp/stunner/blob/main/docs/GATEWAY.md#dataplane).

| Name                                                                  | Description                                                                                                                                          | Value                     |
| --------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------- |
| `stunnerGatewayOperator.dataplane.mode`                               | Dataplane deployment mode. Allowed values: `managed` or `legacy`. | `managed`                 |
| `stunnerGatewayOperator.dataplane.spec.replicas`                      | The replica number of the dataplane to be deployed.                                                                                                  | `1`                       |
| `stunnerGatewayOperator.dataplane.spec.image.name`                    | The name of the image to use for the dataplane.                                                                                                      | `docker.io/l7mp/stunnerd` |
| `stunnerGatewayOperator.dataplane.spec.image.pullPolicy`              | The pull policy for the image.                                                                                                                       | `IfNotPresent`            |
| `stunnerGatewayOperator.dataplane.spec.image.tag`                     | The tag for the image.                                                                                                                               | `1.1.1`                   |
| `stunnerGatewayOperator.dataplane.spec.imagePullSecrets`              | Image pull secrets for the image.                                                                                                                    | `[]`                      |
| `stunnerGatewayOperator.dataplane.spec.command`                       | The command for the image to run on startup.                                                                                                         | `[stunnerd]`              |
| `stunnerGatewayOperator.dataplane.spec.args`                          | The arguments for the image to use with the command.                                                                                                 | `[-w, --udp-thread-num=16]` |
| `stunnerGatewayOperator.dataplane.spec.env`                           | Environment variables to set for the image.                                                                                                          | `[]`                      |
| `stunnerGatewayOperator.dataplane.spec.resources.limits.cpu`          | CPU limits for the container.                                                                                                                        | `2`                       |
| `stunnerGatewayOperator.dataplane.spec.resources.limits.memory`       | Memory limits for the container.                                                                                                                     | `512Mi`                   |
| `stunnerGatewayOperator.dataplane.spec.resources.requests.cpu`        | CPU requests for the container.                                                                                                                      | `500m`                    |
| `stunnerGatewayOperator.dataplane.spec.resources.requests.memory`     | Memory requests for the container.                                                                                                                   | `128Mi`                   |
| `stunnerGatewayOperator.dataplane.spec.terminationGracePeriodSeconds` | Period in seconds to use for graceful shutdown.                                                                                                      | `3600`                    |
| `stunnerGatewayOperator.dataplane.spec.enableMetricsEndpoint`         | If true, enable the metrics endpoint in the deployed STUNner instance.                                                                              | `false`                   |
| `stunnerGatewayOperator.dataplane.spec.hostNetwork`                   | If true, enable host networking in the deployed STUNner instance.                                                                                   | `false`                   |
| `stunnerGatewayOperator.dataplane.spec.labels`                        | Labels to be applied to the deployed stunner instance.                                                                                               | `{}`                      |
| `stunnerGatewayOperator.dataplane.spec.annotations`                   | Annotations to be applied to the deployed stunner instance.                                                                                          | `{}`                      |
| `stunnerGatewayOperator.dataplane.spec.affinity`                      | Affinity settings for the deployed stunner instance.                                                                                                 | `{}`                      |
| `stunnerGatewayOperator.dataplane.spec.securityContext`               | Security context for the deployed stunner instance.                                                                                                  | `{}`                      |
| `stunnerGatewayOperator.dataplane.spec.containerSecurityContext`      | Security context for the container.                                                                                                                  | `{}`                      |
| `stunnerGatewayOperator.dataplane.spec.tolerations`                   | Tolerations for pod assignment.                                                                                                                      | `[]`                      |
| `stunnerGatewayOperator.dataplane.spec.topologySpreadConstraints`     | Constraints to control how pods are spread across the cluster.                                                                                       | `[]`                      |

### STUNner Authentication Service

Default configuration for the authentication service to be deployed. Read more about authentication in STUNner [here](https://github.com/l7mp/stunner/blob/main/docs/AUTH.md).

| Name                                                                            | Description                                                     | Value                                |
| ------------------------------------------------------------------------------- | ----------------------------------------------------------------| ------------------------------------ |
| `stunnerAuthService.enabled`                                                    | If true, deploy the authentication service.                     | `true`                               |
| `stunnerAuthService.deployment.podLabels`                                       | Labels for the auth service pods.                               | `{}`                                 |
| `stunnerAuthService.deployment.affinity`                                        | Affinity settings for the deployed auth-service instance.       | `{}`                                 |
| `stunnerAuthService.deployment.tolerations`                                     | Tolerations for pod assignment.                                 | `[]`                                 |
| `stunnerAuthService.deployment.replicas`                                        | Replicas for the auth-service deployment.                       | `1`                                  |
| `stunnerAuthService.deployment.nodeSelector`                                    | Node labels for pod assignment.                                 | `{kubernetes.io/os: linux}`          |
| `stunnerAuthService.deployment.imagePullSecrets`                                | Image pull secrets for the auth service image.                  | `[]`                                 |
| `stunnerAuthService.deployment.topologySpreadConstraints`                       | Constraints to control how pods are spread across the cluster.  | `[]`                                 |
| `stunnerAuthService.deployment.container.authService.securityContext`           | Security context for the auth-service pod.                      | `{runAsNonRoot: true}`               |
| `stunnerAuthService.deployment.container.authService.image.name`                | The name of the image to use.                                   | `docker.io/l7mp/stunner-auth-server` |
| `stunnerAuthService.deployment.container.authService.image.pullPolicy`          | The pull policy for the image.                                  | `IfNotPresent`                       |
| `stunnerAuthService.deployment.container.authService.image.tag`                 | The tag for the image.                                          | `1.1.1`                              |
| `stunnerAuthService.deployment.container.authService.resources.limits.cpu`      | CPU limits for the container.                                   | `200m`                               |
| `stunnerAuthService.deployment.container.authService.resources.limits.memory`   | Memory limits for the container.                                | `128Mi`                              |
| `stunnerAuthService.deployment.container.authService.resources.requests.cpu`    | CPU requests for the container.                                 | `10m`                                |
| `stunnerAuthService.deployment.container.authService.resources.requests.memory` | Memory requests for the container.                              | `64Mi`                               |
| `stunnerAuthService.deployment.container.authService.args`                      | Arguments for the container.                                    | `[--port=8088, -v]`                  |
