import os
from quixstreams import Application

# for local dev, load env vars from a .env file
from dotenv import load_dotenv
load_dotenv()

app = Application(consumer_group="transformation-v1", auto_offset_reset="earliest")

input_topic = app.topic(os.environ["input"])
output_topic = app.topic(os.environ["output"])

sdf = app.dataframe(input_topic)

def convert_to_sensor_table(row: dict):
    
    for field_key in row["fields"]:
        
        yield {
                "timestamp": row["timestamp"],
                "device_id": row["tags"]["host"],
                "sensor": row["name"],
                "value": row["fields"][field_key],
                "location": "unknown",
                "axis": field_key,
                "tags": row["tags"]
            }

sdf = sdf.apply(convert_to_sensor_table, expand=True)
sdf = sdf.set_timestamp(lambda row: row["timestamp"] / 1E6)
sdf.print()

sdf.to_topic(output_topic)

if __name__ == "__main__":
    app.run()