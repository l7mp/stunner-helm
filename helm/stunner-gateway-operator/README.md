# STUNner Gateway Operator

## Parameters

### STUNner Gateway operator

| Name                                            | Description                                 | Value                      |
| ----------------------------------------------- | ------------------------------------------- | -------------------------- |
| `stunnerGatewayOperator.enabled`                | If enabled, the operator will be installed. | `true`                     |
| `stunnerGatewayOperator.deployment.name`        | Name of the deployment for the operator.    | `stunner-gateway-operator` |
| `stunnerGatewayOperator.deployment.podLabels`   | Labels for the deployment pods.             | `{}`                       |
| `stunnerGatewayOperator.deployment.tolerations` | Tolerations for pod assignment.             | `[]`                       |
