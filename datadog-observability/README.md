# Send Vector logs and metrics to Datadog

In this demo, Vector is running a simple topology in which the `generator` source emits random JSON
logs twice per second and sends those logs off to stdout via the `console` sink. But even this
simple pipeline is enough to generate internal logs and metrics for Vector (via the eponymous
sources).

To run this scenario, make sure you have the `DD_API_KEY` environment variable set to your Datadog
API key and then run:

```bash
docker compose up --detach --remove-orphans
```

Once Vector is up and running, check out the [Logs exporer][logs] and this simple
[Metrics dashboard][metrics].

[logs]: https://app.datadoghq.com/logs?query=%40tag%3Avector
[metrics]: https://app.datadoghq.com/metric/explorer?live=true&tile_size=m&exp_metric=vector.events_in_total&exp_agg=avg&exp_row_type=metric
