# Iceberg Sink

This code sample demonstrates how to consume data from a topic and write the result to an Apache Iceberg table stored in AWS S3 using the AWS Glue Data Catalog.

Modify the Python code to customize the data ingestion and processing logic to suit your needs.

## Overview

The application performs the following steps:

1. **Consume Data**: Reads data from a specified input topic.
2. **Write to Iceberg Table**: Writes the data to an Iceberg table in AWS S3, leveraging AWS Glue as the catalog.

## How to Run

### Prerequisites

- **Python Environment**: Ensure you have Python 3.7 or higher installed.
- **AWS Credentials**: Configure your AWS credentials with appropriate permissions to access S3 and AWS Glue.
- **Dependencies**: Install the required Python packages.

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Set Environment Variables

The application uses the following environment variables:

- **input**: Name of the input topic to listen to.
- **table_name**: The name of the Iceberg table.
- **AWS_S3_URI**: The S3 URI where the Iceberg table data will be stored (e.g., `s3://your-bucket/warehouse/`).
- **AWS_ACCESS_KEY_ID**: Your AWS Access Key ID.
- **AWS_SECRET_ACCESS_KEY**: Your AWS Secret Access Key.
- **AWS_DEFAULT_REGION**: The AWS region where your S3 bucket and AWS Glue catalog are located (e.g., `eu-north-1`).

Create a `.env` file in the project root or set these environment variables in your system.

**Example `.env` file:**

```dotenv
input=your_input_topic
table_name=your_database.your_table
AWS_S3_URI=s3://your-bucket/warehouse/
AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key
AWS_DEFAULT_REGION=eu-north-1
```

**Important Security Note:** **Never** include your actual AWS credentials in code repositories or share them publicly. Always keep your credentials secure.

### Run the Application

```bash
python main.py
```

## Project Structure

- **main.py**: The main entry point of the application.
- **iceberg_sink.py**: Contains the `IcebergSink` class responsible for writing data to the Iceberg table.
- **requirements.txt**: Lists the Python dependencies required for the project.
- **.env**: Contains environment variable definitions (not included in the repository; you need to create it).

## Code Explanation

### `main.py`

```python
from quixstreams import Application
from iceberg_sink import IcebergSink
import os

from dotenv import load_dotenv
load_dotenv()

# Initialize the application with specified consumer group and offset reset policy.
app = Application(
    consumer_group="destination-v2.17",
    auto_offset_reset="earliest",
    commit_interval=5
)

# Get the input topic from environment variables.
input_topic = app.topic(os.environ["input"])

# Initialize the IcebergSink with configuration from environment variables.
iceberg_sink = IcebergSink(
    table_name=os.environ["table_name"],
    aws_s3_uri=os.environ["AWS_S3_URI"],
    s3_region_name=os.environ["AWS_DEFAULT_REGION"]
)

# Create a dataframe from the input topic and attach the sink.
sdf = app.dataframe(input_topic)
sdf.sink(iceberg_sink)

if __name__ == "__main__":
    app.run(sdf)
```

### `iceberg_sink.py`

The `IcebergSink` class handles writing data to an Apache Iceberg table.

Key functionalities:

- **Initialization**: Sets up the Iceberg catalog and table, including schema and partition specification.
- **Data Serialization**: Serializes incoming data batches into Parquet format.
- **Schema Evolution**: Updates the table schema as necessary to accommodate new fields.
- **Data Writing**: Appends data to the Iceberg table.


## Environment Variables

The application uses the following environment variables:

- **input**: Name of the input topic to listen to.
- **table_name**: The fully qualified name of the Iceberg table (e.g., `your_database.your_table`).
- **AWS_S3_URI**: The S3 URI where the Iceberg table data will be stored (e.g., `s3://your-bucket/warehouse/`).
- **AWS_ACCESS_KEY_ID**: Your AWS Access Key ID.
- **AWS_SECRET_ACCESS_KEY**: Your AWS Secret Access Key.
- **AWS_DEFAULT_REGION**: The AWS region where your S3 bucket and AWS Glue catalog are located (e.g., `eu-north-1`).

**Important Security Note:** **Never** include your actual AWS credentials in code repositories or share them publicly. Always keep your credentials secure.

**Example `.env` file:**

```dotenv
input=your_input_topic
table_name=your_database.your_table
AWS_S3_URI=s3://your-bucket/warehouse/
AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key
AWS_DEFAULT_REGION=eu-north-1
```

Replace `your_access_key_id` and `your_secret_access_key` with your actual AWS credentials, but ensure this file is excluded from version control (e.g., add it to your `.gitignore` file).

## Contribute

Submit forked projects to the Quix [GitHub](https://github.com/quixio/quix-samples) repo. Any new project that we accept will be attributed to you, and you'll receive $200 in Quix credit.

## Open Source

This project is open source under the Apache 2.0 license and available in our [GitHub](https://github.com/quixio/quix-samples) repo.

Please star us and mention us on social media to show your appreciation.

## Additional Resources

- **Apache Iceberg Documentation**: [https://iceberg.apache.org/](https://iceberg.apache.org/)
- **AWS Glue Data Catalog**: [https://aws.amazon.com/glue/features/data-catalog/](https://aws.amazon.com/glue/features/data-catalog/)
- **PyIceberg GitHub Repository**: [https://github.com/apache/iceberg/tree/master/python](https://github.com/apache/iceberg/tree/master/python)

## Support

If you encounter any issues or have questions, please reach out through our [GitHub Issues](https://github.com/quixio/quix-samples/issues) page.

---

**Note:** Always practice good security hygiene by keeping your AWS credentials confidential and secure. Consider using AWS IAM roles or AWS Vault for managing credentials securely.
