# STUNner Gateway Operator

## Parameters

### STUNner Gateway operator

| Name                                                                            | Description                                                      | Value                                     |
| ------------------------------------------------------------------------------- | ---------------------------------------------------------------- | ----------------------------------------- |
| `stunnerGatewayOperator.enabled`                                                | If enabled, the operator will be installed.                      | `true`                                    |
| `stunnerGatewayOperator.deployment.name`                                        | Name of the deployment for the operator.                         | `stunner-gateway-operator`                |
| `stunnerGatewayOperator.deployment.podLabels`                                   | Labels for the deployment pods.                                  | `{}`                                      |
| `stunnerGatewayOperator.deployment.tolerations`                                 | Tolerations for pod assignment.                                  | `[]`                                      |
| `stunnerGatewayOperator.deployment.nodeSelector`                                | Node labels for pod assignment.                                  | `{}`                                      |
| `stunnerGatewayOperator.deployment.imagePullSecrets`                            | Image pull secrets for the image.                                | `[]`                                      |
| `stunnerGatewayOperator.deployment.container`                                   | Container configuration values.                                  |                                           |
| `stunnerGatewayOperator.deployment.container.manager`                           | Configuration values for the STUNner Gateway Operator container. |                                           |
| `stunnerGatewayOperator.deployment.container.manager.image.name`                | The name of the image to use.                                    | `docker.io/l7mp/stunner-gateway-operator` |
| `stunnerGatewayOperator.deployment.container.manager.image.pullPolicy`          | The pull policy for the image.                                   | `IfNotPresent`                            |
| `stunnerGatewayOperator.deployment.container.manager.image.tag`                 | The tag for the image.                                           | `1.0.0`                                   |
| `stunnerGatewayOperator.deployment.container.manager.resources.limits.cpu`      | CPU limits for the container.                                    | `1000m`                                   |
| `stunnerGatewayOperator.deployment.container.manager.resources.limits.memory`   | Memory limits for the container.                                 | `512Mi`                                   |
| `stunnerGatewayOperator.deployment.container.manager.resources.requests.cpu`    | CPU requests for the container.                                  | `250m`                                    |
| `stunnerGatewayOperator.deployment.container.manager.resources.requests.memory` | Memory requests for the container.                               | `128Mi`                                   |
| `stunnerGatewayOperator.deployment.container.manager.args`                      | Arguments for the container.                                     | `[]`                                      |
| `stunnerGatewayOperator.deployment.container.kubeRbacProxy`                     | Configuration values for the Kube RBAC Proxy container.          |                                           |
| `stunnerGatewayOperator.deployment.container.kubeRbacProxy.image.name`          | The name of the image to use.                                    | `gcr.io/kubebuilder/kube-rbac-proxy`      |
| `stunnerGatewayOperator.deployment.container.kubeRbacProxy.image.pullPolicy`    | The pull policy for the image.                                   | `IfNotPresent`                            |
| `stunnerGatewayOperator.deployment.container.kubeRbacProxy.image.tag`           | The tag for the image.                                           | `v0.16.0`                                 |

### Dataplane

Default dataplane configuration for the operator to use. See more [here](https://github.com/l7mp/stunner/blob/main/docs/GATEWAY.md#dataplane).

| Name                                                                  | Description                                                                                                                                          | Value                     |
| --------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------- |
| `stunnerGatewayOperator.dataplane.mode`                               | Mode to use for the deployment of the dataplane. Can be either `managed` or `legacy`. Read about the modes [here](stunnerGatewayOperator.dataplane). | `managed`                 |
| `stunnerGatewayOperator.dataplane.spec.replicas`                      | The replica number of the dataplane to be deployed.                                                                                                  | `1`                       |
| `stunnerGatewayOperator.dataplane.spec.image.name`                    | The name of the image to use for the dataplane.                                                                                                      | `docker.io/l7mp/stunnerd` |
| `stunnerGatewayOperator.dataplane.spec.image.pullPolicy`              | The pull policy for the image.                                                                                                                       | `IfNotPresent`            |
| `stunnerGatewayOperator.dataplane.spec.image.tag`                     | The tag for the image.                                                                                                                               | `1.0.0`                   |
| `stunnerGatewayOperator.dataplane.spec.command`                       | The command for the image to run on startup.                                                                                                         | `[]`                      |
| `stunnerGatewayOperator.dataplane.spec.args`                          | The arguments for the image to use with the command.                                                                                                 | `[]`                      |
| `stunnerGatewayOperator.dataplane.spec.env`                           | Environment variables to set for the image.                                                                                                          | `[]`                      |
| `stunnerGatewayOperator.dataplane.spec.resources.limits.cpu`          | CPU limits for the container.                                                                                                                        | `2`                       |
| `stunnerGatewayOperator.dataplane.spec.resources.limits.memory`       | Memory limits for the container.                                                                                                                     | `512Mi`                   |
| `stunnerGatewayOperator.dataplane.spec.resources.requests.cpu`        | CPU requests for the container.                                                                                                                      | `500m`                    |
| `stunnerGatewayOperator.dataplane.spec.resources.requests.memory`     | Memory requests for the container.                                                                                                                   | `128Mi`                   |
| `stunnerGatewayOperator.dataplane.spec.terminationGracePeriodSeconds` | Period in seconds to use for graceful shutdown.                                                                                                      | `3600`                    |
| `stunnerGatewayOperator.dataplane.spec.enableMetricsEndpoint`         | Enable metrics endpoint in the deployed stunner instance.                                                                                            | `false`                   |
| `stunnerGatewayOperator.dataplane.spec.hostNetwork`                   | Enable host networking in the deployed stunner instance.                                                                                             | `false`                   |
| `stunnerGatewayOperator.dataplane.spec.labels`                        | Labels to be applied to the deployed stunner instance.                                                                                               | `{}`                      |
| `stunnerGatewayOperator.dataplane.spec.annotations`                   | Annotations to be applied to the deployed stunner instance.                                                                                          | `{}`                      |
| `stunnerGatewayOperator.dataplane.spec.affinity`                      | Affinity settings for the deployed stunner instance.                                                                                                 | `{}`                      |
| `stunnerGatewayOperator.dataplane.spec.securityContext`               | Security context for the deployed stunner instance.                                                                                                  | `{}`                      |
| `stunnerGatewayOperator.dataplane.spec.tolerations`                   | Tolerations for pod assignment.                                                                                                                      | `[]`                      |

### STUNner Authentication Service

Default configuration for the authentication service to be deployed. See more the authentication in STUNner [here](https://github.com/l7mp/stunner/blob/main/docs/AUTH.md).

| Name                                                                            | Description                                              | Value                                |
| ------------------------------------------------------------------------------- | -------------------------------------------------------- | ------------------------------------ |
| `stunnerAuthService.enabled`                                                    | If enabled, the authentication service will be deployed. | `true`                               |
| `stunnerAuthService.deployment.podLabels`                                       | Labels for the auth service pods.                        | `{}`                                 |
| `stunnerAuthService.deployment.tolerations`                                     | Tolerations for pod assignment.                          | `[]`                                 |
| `stunnerAuthService.deployment.nodeSelector`                                    | Node labels for pod assignment.                          |                                      |
| `stunnerAuthService.deployment.imagePullSecrets`                                | Image pull secrets for the auth service image.           | `[]`                                 |
| `stunnerAuthService.deployment.container.authService.image.name`                | The name of the image to use.                            | `docker.io/l7mp/stunner-auth-server` |
| `stunnerAuthService.deployment.container.authService.image.pullPolicy`          | The pull policy for the image.                           | `IfNotPresent`                       |
| `stunnerAuthService.deployment.container.authService.image.tag`                 | The tag for the image.                                   | `1.0.0`                              |
| `stunnerAuthService.deployment.container.authService.resources.limits.cpu`      | CPU limits for the container.                            | `200m`                               |
| `stunnerAuthService.deployment.container.authService.resources.limits.memory`   | Memory limits for the container.                         | `128Mi`                              |
| `stunnerAuthService.deployment.container.authService.resources.requests.cpu`    | CPU requests for the container.                          | `10m`                                |
| `stunnerAuthService.deployment.container.authService.resources.requests.memory` | Memory requests for the container.                       | `64Mi`                               |
| `stunnerAuthService.deployment.container.authService.args`                      | Arguments for the container.                             | `[]`                                 |
