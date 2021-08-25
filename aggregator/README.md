# Vector aggregator demo

## How to start it

```shell
docker-compose up --detach
```

This starts up the full scenario in the background, which includes:

* A Vector [aggregator]
* 10 Vector [agents][agent] feeding JSON logs into the aggregator

You can see the aggregator output in real-time by running this command:

```shell
docker-compose logs --follow aggregator
```

[agent]: https://vector.dev/docs/setup/deployment/roles/#agent
[aggregator]: https://vector.dev/docs/setup/deployment/roles/#aggregator