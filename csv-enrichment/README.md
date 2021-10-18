# CSV enrichment in Vector

> **Note:** This feature is unreleased and still under active development. However, if you want to try it out, we would
> love any feedback!

## How to start it

```shell
docker-compose up
```

## What it does

This demo shows an example of using CSV enrichment in Vector to enrich events with data from two CSV files.

The [`users.csv`](./data/users.csv) file contains a list of users with their phone numbers and addresses, while the
[`codes.csv`](./data/codes.csv) file contains a list of common Unix exit codes (with code, tag, and message info).

The [`vector.toml`](./vector.toml) configuration contains:

* Two `generator` sources in the that generate fake events that can be enriched using the CSV files (user data and coded error messages
  respectively)
* Two `remap` transforms that parse the events and then look up the corresponding records from the CSV files to enrich the events with more metadata
* A `console` sink to print out the events
