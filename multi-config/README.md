# Composing Vector Config Files
This repo is a simple demonstration of providing Vector with multiple `ConfigMap` files from a Kubernetes cluster. By
leveraging this, users can break apart pieces of their Vector configs for management by multiple business units.

## Constraints
* **This solution works inside of a vanilla Kubernetes cluster.** This is intended as a simple solution that any
  customer can easily hit the ground running with.
* **Helm does not support templating in `values.yaml`.** [The method we use to provide extra config files to Vector does not support templated names](https://github.com/helm/helm/issues/2492),
  which makes it difficult to make this a truly generic solution for your needs. In particular, this makes it
  impossible to properly scope the ConfigMap names with `{{ .Release.Name }}` as you might wish.

## The Basics
Multiple configs are provided to Vector by wrapping the official Helm chart with this one, which generates a ConfigMap
from a directory and adds that to the supported `extraConfigDirSources` for the Vector pod.

To add configs to Vector in this setup, all you must do is add them to the `./vector` directory: both the locally-running
Vector as well as the one installed by the Helm chart are configured to utilize all files there. Only `.yaml` files are
supported for now.

A simple `Makefile` is supplied which demonstrates the proper commands to test this setup both locally and through Helm.
Teardown commands are also provided there for when testing is complete.

The Helm chart was tested in `minikube` running on an EC2 instance.

## Next Steps
While useful, this setup does have limitations. In particular, the configs must be managed and provisioned inside of the
same Kubernetes cluster that Vector runs in. Managing multiple clusters still imposes a non-trivial operational overhead.
[Helm's template control structures](https://helm.sh/docs/chart_template_guide/control_structures/) could provide some
ways of providing for multiple kinds of clusters/deployments from a single chart, although doing so is beyond the scope
of this demo.

Datadog's Observability Pipelines feature set (coming soon) can more easily provide config synchronization between a
fleet of Vector instances, and allow remote management of Vector in an easy-to-use UI. If you're interested, please
contact your TAM or Datadog Sales for more information on pricing and timelines.