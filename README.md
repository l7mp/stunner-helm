# STUNner Helm charts


## Important
There are a few things to know before jumping right into using stunner
- STUNner must installed into the same namespace as the gatewayclass and config was in case you are using STUNner with the gateway-operator

There are two ways to install and use STUNner.

### With the STUNner Gateway Operator

```
helm repo add stunner https://l7mp.io/stunner
helm repo update

helm install stunner-gateway-operator stunner/stunner-gateway-operator

helm install stunner stunner/stunner
```

### Without the Operator in Standalone Mode 

```
helm repo add stunner https://l7mp.io/stunner
helm repo update

helm install stunner stunner/stunner --set stunner.standalone.enabled=true
```