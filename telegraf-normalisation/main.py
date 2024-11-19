import os
from quixstreams import Application
import json

# for local dev, load env vars from a .env file
from dotenv import load_dotenv
load_dotenv()

app = Application(consumer_group="transformation-v1", auto_offset_reset="earliest")

input_topic = app.topic(os.environ["input"])
output_topic = app.topic(os.environ["output"])

sdf = app.dataframe(input_topic)

def convert_to_sensor_table(row: dict):
    
    for field_key in row["fields"]:
        
        output_row = {
                "timestamp": row["timestamp"],
                "device_id": row["tags"]["host"],
                "sensor": row["name"],
                "location": json.dumps(row["tags"]),
                "axis": field_key,
            }
        
        value = row["fields"][field_key]

        if isinstance(value, (int, float)):  # Check for number (integer or float)
            output_row["value_float"] =  float(value)
        elif isinstance(value, str):  # Check for string
            output_row["value_str"] = str(value)
        else:
            print(f"{value} is neither a number nor a string")
            
        yield output_row

sdf = sdf.apply(convert_to_sensor_table, expand=True)
sdf = sdf.set_timestamp(lambda row: row["timestamp"] / 1E6)
sdf.print()

sdf.to_topic(output_topic)

if __name__ == "__main__":
    app.run()
    
            