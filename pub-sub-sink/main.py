import os
from google.api_core import retry
from google.cloud.pubsub_v1.types import PublisherOptions
from quixstreams import Application
from quixstreams.sinks.community.bigquery import PubSubSink
import json

# for local dev, load env vars from a .env file
from dotenv import load_dotenv
load_dotenv()

TOPIC_ID = os.environ["TOPIC_ID"]
PROJECT_ID = os.environ["PROJECT_ID"]
SERVICE_ACCOUNT_JSON = os.environ["SERVICE_ACCOUNT_JSON"]


# Configure the sink
pubsub_sink = PubSubSink(
    project_id=PROJECT_ID,
    topic_id=TOPIC_ID,
    # Optional: service account credentials as a JSON string
    service_account_json=SERVICE_ACCOUNT_JSON,
    # Optional: customize serialization and flush timeout
    value_serializer=json.dumps,
    key_serializer=str,
    flush_timeout=10,
    # Optional: Additional keyword arguments are passed to the PublisherClient
    publisher_options=PublisherOptions(
        # Configure publisher options to retry on any exception
        retry=retry.Retry(predicate=retry.if_exception_type(Exception)),
    )
)

app = Application(
    consumer_group=os.environ["CONSUMER_GROUP"], 
    auto_offset_reset = "earliest",
    commit_interval=1,
    commit_every=100)

input_topic = app.topic(os.environ["input"])

sdf = app.dataframe(input_topic)
sdf.sink(pubsub_sink)

if __name__ == "__main__":
    app.run(sdf)