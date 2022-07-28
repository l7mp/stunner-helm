# STUNner Helm charts


## Important
There are a few things to know before jumping right into using stunner
- STUNner must installed into the same namespace as the gatewayclass and config was in case you are using STUNner with the gateway-operator

## Deploying
There are two ways to install and use STUNner. It is advised to use STUNner with the STUNner Gateway Operator.

### With the STUNner Gateway Operator

```
helm repo add stunner https://l7mp.io/stunner
helm repo update

helm install stunner-gateway-operator stunner/stunner-gateway-operator --create-namespace --namespace=<your-namespace>

helm install stunner stunner/stunner --create-namespace --namespace=<your-namespace>
```

### Without the Operator in Standalone Mode 

```
helm repo add stunner https://l7mp.io/stunner
helm repo update

helm install stunner stunner/stunner --set stunner.standalone.enabled=true --create-namespace --namespace=<your-namespace> 
```