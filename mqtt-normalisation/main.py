import os
from quixstreams import Application

# for local dev, load env vars from a .env file
from dotenv import load_dotenv
load_dotenv()

app = Application(
    consumer_group="mqtt-norm-v1", 
    auto_offset_reset="earliest",
    processing_guarantee="exactly-once")

input_topic = app.topic(os.environ["input"], value_deserializer="bytes", key_deserializer="str")
output_topic = app.topic(os.environ["output"])


sdf = app.dataframe(input_topic)

sdf = sdf.filter(lambda row, key, *_: len(key.split("-")) == 6, metadata=True)

def expand_key(row, key, timestamp, headers):
    
    expanded_key = key.split("-")
    
    return {
        "device_id": expanded_key[3],
        "sensor": expanded_key[0],
        "axis": expanded_key[2],
        "location": expanded_key[4],
        "timestamp": timestamp,
        "value": bytes.decode(row)
    }

sdf = sdf.apply(expand_key, metadata=True)
sdf = sdf.set_timestamp(lambda row, *_: row["timestamp"])
sdf = sdf.drop("timestamp")
sdf.print()
sdf.to_topic(output_topic)

if __name__ == "__main__":
    app.run()