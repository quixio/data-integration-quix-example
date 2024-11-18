import os
from quixstreams import Application
from datetime import datetime

# for local dev, load env vars from a .env file
from dotenv import load_dotenv
load_dotenv()

app = Application(consumer_group="postgres-norm-v1.1", auto_offset_reset="earliest")

input_topic = app.topic(os.environ["input"])
output_topic = app.topic(os.environ["output"])

sdf = app.dataframe(input_topic)

def convert_to_sensor_table(row: dict):
    
    result = {}
    for i in range(len(row["columnnames"])):
        result[row["columnnames"][i]] = row["columnvalues"][i]
        
    return result

def expand_row(row: dict):
    
    fixed_fields = ["timestamp","__key","sessionId","deviceId"]
    
    if "location-latitude" in row and "location-longitude" in row:
        location = f"{row['location-latitude']},{row['location-longitude']}"
    else:
        location = "unknown"
    
    for key in row:
        
        if key in fixed_fields:
            continue
        
        key_parts = key.split("-")
        
        if len(key_parts) != 2:
            continue
        
        yield {
            "timestamp": datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S.%f").timestamp() * 1000,
            "device_id": row["deviceId"],
            "sensor": key_parts[0],
            "value": row[key],
            "location": location,
            "axis": key_parts[1]
        }

sdf = sdf.apply(convert_to_sensor_table)

sdf = sdf.apply(expand_row, expand=True)

sdf.print()
sdf.to_topic(output_topic)

if __name__ == "__main__":
    app.run()