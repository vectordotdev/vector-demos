# Datadog Agent account routing

This demo demonstrates how to use Vector to ingest logs, metrics, and traces
from the Datadog Agent and route them to different Datadog accounts. In this
case, it routes them by Kubernetes namespace, but the example can be adapted to
your use case.

## Prerequisites

- [helm](https://helm.sh/docs/intro/install/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [minikube](https://minikube.sigs.k8s.io/docs/start/)

Three Datadog accounts:

- One root one for observability data outside of the application namespaces
- One for applications running in the `foo` namespace we will create below
- One for applications running in the `bar` namespace we will create below

You can also run this demo with one Datadog account by setting the Datadog API
key to the same value for all three when exporting the environment variables
below.

## Running the demo

Start minikube:

```shell
minikube start
```

Add the necessary Helm repositories for the Vector and Datadog charts:

```shell
helm repo add datadog https://helm.datadoghq.com
helm repo add vector https://helm.vector.dev
helm repo update
```

We will be deploying two demo apps in two different namespaces.

Start by exporting the needed Datadog API keys (replacing the `...`s):

```shell
# this should be the key you want data to go to when it is in the kube-system,
# default, or an unknown namespace
export DD_API_KEY=...
# this should be the key you want data to go when it is from the `foo` namespace
export DD_API_KEY_FOO=...
# this should be the key you want data to go when it is from the `bar` namespace
export DD_API_KEY_BAR=...
```

Build the demo app that we will deploy to the `foo` and `bar` namespaces:

```shell
docker build --file test-app/Dockerfile --tag test-app:latest test-app
```

And upload to minikube:

```shell
minikube image load test-app:latest
```

We will now deploy demo app to both the `foo` and `bar` namespaces:

```shell
kubectl create namespace foo
kubectl create namespace bar
kubectl apply --namespace foo --filename test-app/deployment.yaml
kubectl apply --namespace bar --filename test-app/deployment.yaml
```

Now that we have the demo app running in both namespaces, let's deploy the
Datadog agent to collect its telemetry. The demo app generates logs, metrics,
and traces.

```shell
helm install datadog-agent -f datadog.values.yaml --set datadog.apiKey=$DD_API_KEY datadog/datadog
```

With the Datadog Agent installed, we can deploy Vector to route the
observability data.

Start by creating a config map to hold the Kubernetes namespace -> Datadog API
key mapping. We will use this with Vector's [CSV enrichment
feature](https://vector.dev/highlights/2021-11-18-csv-enrichment/) to lookup the
API key to use by namespace.

```shell
cat <<-EOF > api-keys-config-map.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: "namespace-api-keys-configmap"
data:
  namespace-api-keys.csv: |
    namespace,api_key
    default,$DD_API_KEY
    kube_system,$DD_API_KEY
    unknown,$DD_API_KEY
    foo,$DD_API_KEY_FOO
    bar,$DD_API_KEY_BAR
EOF
```

In the real world, you will probably want to load these as secrets, but here we
use plaintext for simplicity. You can see here that we map the `foo` and `bar`
namespaces to their respective API keys and the rest are mapped to `DD_API_KEY`.
The `unknown` namespace will be for when Vector cannot find the namespace on the
incoming data (usually indicating the logs or metrics refer to the kubernetes
control plane).

Now deploy Vector:

```shell
helm install vector vector/vector --values vector.values.yaml
```

Once Vector is deployed, you will see data flowing into each of your Datadog
accounts.

## Cleaning up

You can run `minikube delete` to teardown all resources.
