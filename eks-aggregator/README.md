# EKS Stateless Aggregator Demo

## Prerequisites

- [helm](https://helm.sh/docs/intro/install/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [ekctl](https://eksctl.io/introduction/#installation) - if creating a new cluster with the Makefile

Your EKS cluster will need the [AWS Load Balancer Controller](https://github.com/kubernetes-sigs/aws-load-balancer-controller) installed, this will be installed via the `make` targets or you
can follow [Amazon's instructions](https://docs.aws.amazon.com/eks/latest/userguide/aws-load-balancer-controller.html) for your own cluster. Additionally you'll also need a Datadog API key for Vector and the Datadog Agents.

## Getting started

Add the necessary Helm repositories for the Vector and Datadog charts:

```shell
helm repo add datadog https://helm.datadoghq.com
helm repo add vector https://helm.vector.dev
helm repo update
```

If you need to provision an EKS cluster with the AWS load balancer controller, you can use the included Makefile by running:

```shell
ACCOUNT_ID=<AWS_ACCOUNT_ID> make cluster-up
```

The following command will install Vector as an Aggregator using an Application Load Balancer to route requests from Datadog Agents.
Vector is configured to process Datadog Agent logs in a similar fashion Datadog's [Pipelines](https://docs.datadoghq.com/logs/log_configuration/pipelines/)
feature, allowing you to move your log processing onto your own hardware.

```shell
helm upgrade --install vector vector/vector --devel \
	--namespace vector --values helm/vector.yaml \
	--set secrets.generic.DATADOG_API_KEY=<DD_API_KEY(base64 encoded)> \
	--set ingress.hosts[0].host=DUMMY_VAL
```

Once your ALB is provisioned you can run the following command to extract it's generated hostname to replace the DUMMY_VAL above.

```shell
export ALB_HOSTNAME=kubectl --namespace vector get ingress vector \
	--output go-template='{{(index .status.loadBalancer.ingress 0 ).hostname}}'
```

The following command will upgrade your `vector` release with the created ALB hostname.

```shell
helm upgrade --install vector vector/vector --devel \
	--namespace vector --values helm/vector.yaml \
	--set secrets.generic.DATADOG_API_KEY=<DD_API_KEY(base64 encoded)> \
	--set ingress.hosts[0].host=${ALB_HOSTNAME}
```

Then install your Datadog Agents substituting the hostname from the previous step.

```shell
helm upgrade --install datadog datadog/datadog \
	--namespace datadog --values helm/datadog.yaml \
	--set datadog.apiKey=<DD_API_KEY> \
	--set agents.customAgentConfig.logs_config.logs_dd_url="<ALB_HOSTNAME>:8080"
	```

Once all the pods have started, you should begin to see logs being ingested to your [Datadog account](https://app.datadoghq.com/logs) that are being aggregated and parsed by Vector.

## Cleaning up

The _cluster-down_ target will delete the Namespaces and Cluster created during this demo.

```shell
make cluster-down
```

## Notes

- A nightly image is currently used to leverage our rewritten `datadog_logs` sink
- The `--devel` option is used to access our currently _pre-release_ [`vector`](https://github.com/vectordotdev/helm-charts/blob/develop/charts/vector/README.md) chart
