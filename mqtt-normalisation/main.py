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
    sensor_id = f"{expanded_key[0]}-{expanded_key[1]}-{expanded_key[2]}"
    
    

    result = {
        "device_id": expanded_key[4],
        "sensor": sensor_id,
        "axis": expanded_key[3],
        "location": expanded_key[5],
        "timestamp": timestamp
    }
    
    value = bytes.decode(row)
    
    if isinstance(value, (int, float)):  # Check for number (integer or float)
        result["value_float"] =  float(value)
    elif isinstance(value, str):  # Check for string
        result["value_str"] = str(value)
    else:
        print(f"{value} is neither a number nor a string")
        
    return result

sdf = sdf.apply(expand_key, metadata=True)
sdf = sdf.set_timestamp(lambda row, *_: row["timestamp"])
sdf = sdf.drop("timestamp")
sdf.print()
sdf.to_topic(output_topic)

if __name__ == "__main__":
    app.run()