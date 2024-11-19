from quixstreams import Application
from quixstreams.sinks.community.iceberg import IcebergSink, AWSIcebergConfig

from pyiceberg.transforms import DayTransform, IdentityTransform
from pyiceberg.partitioning import PartitionSpec, PartitionField
from pyiceberg.schema import Schema, NestedField
from pyiceberg.types import StringType, TimestampType, LongType


import os

from dotenv import load_dotenv
load_dotenv()

app = Application(consumer_group="aws-iceberg-sink-v1", 
                  auto_offset_reset = "earliest",
                  commit_interval=5)

input_topic = app.topic(os.environ["input"])


def get_default_schema() -> Schema:
        """
        Return a default Iceberg schema when none is provided.
        """
        return Schema(
            fields=(
                NestedField(
                    field_id=1,
                    name="_timestamp",
                    field_type=TimestampType(),
                    required=False,
                ),
                NestedField(
                    field_id=2, name="device_id", field_type=StringType(), required=False
                ),
                NestedField(
                    field_id=3, name="sensor", field_type=StringType(), required=False
                ),
                NestedField(
                    field_id=4, name="axis", field_type=StringType(), required=False
                ),
            )
        )

def get_default_partition_spec(schema: Schema) -> PartitionSpec:
    """
    Set up a default partition specification if none is provided.
    """
    # Map field names to field IDs from the schema.
    field_ids = {field.name: field.field_id for field in schema.fields}

    # Create partition fields for kafka key and timestamp.
    partition_fields = (
        PartitionField(
            source_id=field_ids["_timestamp"],
            field_id=1000,
            transform=DayTransform(),
            name="day",
        ),
        PartitionField(
            source_id=field_ids["device_id"],
            field_id=1001,  # Unique partition field ID.
            transform=IdentityTransform(),
            name="device_id",
        ),
        PartitionField(
            source_id=field_ids["sensor"],
            field_id=1002,  # Unique partition field ID.
            transform=IdentityTransform(),
            name="sensor",
        ),
        PartitionField(
            source_id=field_ids["axis"],
            field_id=1003,  # Unique partition field ID.
            transform=IdentityTransform(),
            name="axis",
        )
    )

    # Create the new PartitionSpec.
    return PartitionSpec(fields=partition_fields)



iceberg_sink = IcebergSink(
    data_catalog_spec="aws_glue",
    table_name=os.environ["table_name"],
    schema=get_default_schema(),
    partition_spec=get_default_partition_spec(get_default_schema()),
    config=AWSIcebergConfig(
        aws_s3_uri=os.environ["AWS_S3_URI"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
        aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
        aws_region=os.environ["AWS_REGION"]))

sdf = app.dataframe(input_topic)
sdf = sdf[sdf.contains("value_float") or sdf.contains("value_str")]

sdf["value_float"] = sdf.apply(lambda row: row["value_float"] if "value_float" in sdf else None)
sdf["value_str"] = sdf.apply(lambda row: row["value_str"] if "value_str" in sdf else None)

sdf = sdf[["device_id", "sensor","axis","location","value_float", "value_str"]]

sdf.sink(iceberg_sink)

if __name__ == "__main__":
    app.run(sdf)