# Fake program for generating logs, traces, and metrics for demonstration

from prometheus_client import start_http_server, Summary
import logging
import random
import time
import os
from ddtrace import tracer

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

# Decorate function with metric.
@REQUEST_TIME.time()
# Trace function.
@tracer.wrap('process_request', service="vector-demo-test-app")
def process_request():
    time.sleep(random.random())
    logging.info("request processed")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    tracer.configure(
        hostname="127.0.0.1",
        port="8126",
    )

    # Start up the server to expose the metrics.
    start_http_server(9100)

    # Generate fake requests.
    while True:
        process_request()
