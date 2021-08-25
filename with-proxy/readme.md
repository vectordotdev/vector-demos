# Vector integration with a proxy

For this demo, we'll use Squid as a proxy and [`nginx_metrics`](https://vector.dev/docs/reference/configuration/sources/nginx_metrics/) as source component.

## How to start it

To start it, you first need to clone this repository, go into the `with-proxy` folder and run `docker-compose up`.

## What it does.

The [`docker-compose.yml`](./docker-compose.yml) declares 2 times of network. The `public` network to which only Vector and Squid have access, and the `private` to which only Nginx and Squid have access. Vector and Nginx can't communicate with each other.

To allow Vector to reach Nginx, the proxy configuration has to be set on Vector. It can be done in 3 different ways:
- with an environment variable, by setting `HTTP_PROXY=http://squid:3128`, see the comment in [`docker-compose.yml`](./docker-compose.yml).
- by setting the proxy globaly, like in the first three lines of [`vector/vector.toml`](./vector/vector.toml).
- by setting the proxy at the component level, in the section `[sources.nginx.proxy]` of [`vector/vector.toml`](./vector/vector.toml).

This way, Vector will send the polling requests to Nginx through Squid.