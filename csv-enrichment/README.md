# CSV enrichment in Vector

**Note:** This feature is unreleased and still under active development. However, if you want to try it out, we would
love any feedback!

## How to start it

`docker-compose up`

## What it does

This demo shows an example of using CSV enrichment in Vector to enrich events with data from a CSV file.

The CSV file ([`./data/users.csv`](./data/users.csv) contains a list of users with their phone numbers and addresses.

The `vector.toml` configuration contains:

* A `random` source in the `vector.toml` that simply generates some fake events using names that match users in the CSV file
* A `remap` transform then parses these events and then looks up the corresponding record from the CSV file to enrich the event with more metadata
* A `console` sink to print out the events
