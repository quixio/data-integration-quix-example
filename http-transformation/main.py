import os
from quixstreams import Application

# for local dev, load env vars from a .env file
from dotenv import load_dotenv
load_dotenv()

app = Application(consumer_group="v1.1", 
            auto_offset_reset="earliest", 
            use_changelog_topics=False)

input_topic = app.topic(os.environ["input"], key_deserializer="str")
output_topic = app.topic(os.environ["output"])

sdf = app.dataframe(input_topic)

sdf = sdf.apply(lambda row: row["payload"], expand=True)

# Calculate hopping window of 5 seconds with 10 second buffer delay.
sdf = sdf.tumbling_window(1000, 10000).collect().final()

sdf = sdf.apply(lambda row: sorted(row["value"], key=lambda row: row["time"]), expand=True)

def transpose(row, key, *_):

    for axis, value in row["values"].items():
        yield {
            "device_id": key,
            "sensor": row["name"],
            "axis": axis,
            "location": "na",
            "timestamp": row["time"],
            "value": value
        }

sdf = sdf.apply(transpose, metadata=True, expand=True) 
        
# Print JSON messages in console.
sdf.print_table(metadata=False)

# Send the message to the output topic
sdf.to_topic(output_topic)

if __name__ == "__main__":
    app.run()