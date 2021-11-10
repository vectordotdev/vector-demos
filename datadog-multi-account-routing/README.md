# Routing events to multiple Datadog accounts

This demo provides an example of routing events to multiple Datadog accounts
based on event metadata. It includes:

* Collecting container logs in Kubernetes via the Datadog Agent
* Sending those logs to a Vector aggregator
* Routing all events to one root acocunt
* Routing subsets of events to other accounts based on event metadata (here
  Kubernetes namespaces)

This is meant to be an illustrative example of how to combine different
components of Vector. If you have any questions or issues running this demo,
please [let us know!](https://github.com/vectordotdev/vector-demos/discussions).

## How to run it

First, you need to generate a few Datadog API keys. If you want to fully
experiment with this setup, it is recommended to generate them in separate
accounts, but you can also generate them in one account for testing.

To generate a Datadog API key head [here in Europe](https://app.datadoghq.eu/account/settings#api) or [here in the US](https://app.datadoghq.com/account/settings#api).

You'll want to generate three keys and export them as environment variables:

* One for the root account you want all events to go to. Export as `DD_API_KEY`.
* One for subaccount A where only events in the `subaccount_a` Kubernetes namespace will be
  sent. Export as `SUBACCOUNT_A_DD_API_KEY`.
* One for subaccount B where only events in the `subaccount_b` Kubernetes namespace will be
  sent. Export as `SUBACCOUNT_B_DD_API_KEY`.

Then you'll want to start up [minikube](https://minikube.sigs.k8s.io/docs/):

```sh
minikube start
```

You'll then want to deploy Vector as an aggregator via [Helm](https://helm.sh)
to receive logs from the Datadog agent we'll install later:

```
helm repo add vector https://helm.vector.dev
helm repo update

helm install --name vector vector/vector # TODO config
```

We'll go over the configuration the aggregator is using below.

Next, install the Datadog Agent to collect local cluster logs:

```

```

Now we are ready to deploy some dummy applications to have their logs shipped to
our three Datadog accounts.

First, create two namespaces to deploy the applications in. Vector will route
the logs to the Datadog accounts based on the namespace (you could also
route based on other metadata!):

```
```

Next, some dummy applications to log into these namespaces:

```
```

Finally, check out your logs in your Datadog accounts!

You will find:

* Logs from the application in the `subaccount_a` namespace are sent to both the
  root account (associated with `$DD_API_KEY`) as well as the subaccount
  A (associated with `$SUBACCOUNT_A_DD_API_KEY`)
* Logs from the application in the `subaccount_b` namespace are sent to both the
  root account (associated with `$DD_API_KEY`) as well as the subaccount
  A (associated with `$SUBACCOUNT_B_DD_API_KEY`)

## How it works
