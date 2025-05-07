import os
from quixstreams import Application

# for local dev, load env vars from a .env file
from dotenv import load_dotenv
load_dotenv()

app = Application(consumer_group="v1.1", 
            auto_offset_reset="earliest", 
            use_changelog_topics=False)

input_topic = app.topic(os.environ["input"])
output_topic = app.topic(os.environ["output"])

sdf = app.dataframe(input_topic)

sdf = sdf.apply(lambda row: row["payload"], expand=True)

# Calculate hopping window of 10 minutes with 3 buffer delay.
sdf = sdf.tumbling_window(3600, 3000).collect().final()

sdf = sdf.apply(lambda row: sorted(row["value"], key=lambda row: row["time"), expand=True)

        
# Print JSON messages in console.
sdf.print()

# Send the message to the output topic
#sdf.to_topic(output_topic)

if __name__ == "__main__":
    app.run()