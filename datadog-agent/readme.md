# Vector integration with Datadog Agent

![logs on datadog interface](./result.png)

## How to start it

First you need to get an API key from Datadog ([here in Europe](https://app.datadoghq.eu/account/settings#api) or [here in the US](https://app.datadoghq.com/account/settings#api)) and then you just need to run `DD_API_KEY=<your-api-key> docker-compose up`.

## What it does

### Datadog Agent

The Datadog Agent configuration is split in two files.

The `agent/datadog.yaml` file contains a `log_config` section, to tell the Agent to forward the logs to Vector and `logs_enabled` to tell the Agent to gather the logs. Considering we are using `docker-compose`, Vector will be reachable with the hostname `vector` (the name of the service in the `docker-compose.yml` file).

The second file is `agent/conf.d/test.d/conf.yaml` in which we specify where to go read the logs.

### Vector

The `vector/vector.toml` configuration is split in two parts.
The `generator` part is used to create random logs to feed the agent. It's only relevant for this demo and should be removed in real life usage.
The `configuration` where the `agent` source and the `datadog` sink are configured. 

The `agent` source uses the [`datadog_agent` source component](https://master.vector.dev/docs/reference/configuration/sources/datadog_agent/) which allows to receive the logs collected by the Datadog Agent. Vector will then expose a http server behaving like the Datadog's servers and aggregate all the logs sent by the agents.

The `datadog` sink uses the [`datadog_logs` sink component](https://master.vector.dev/docs/reference/configuration/sinks/datadog_logs/) which allows to send any logs to Datadog. Vector will then take all the logs it receives, batch them and send them right away to Datadog.

In the current configuration, Vector acts like an agregator. This allows you to do some filtering and transformation treatments before leaving your network and reaching Datadog. This allows you to reduce your network bill, considering you can keep all those treatments in the same network area (for example, without going out of AWS).
