# Iceberg Query
This is super simple frontend to query AWS Apache Iceberg using AWS Athena. 

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
- **basic_auth_password** Password for frontend basic auth
- **table_name**: The name of the Iceberg table.
- **AWS_S3_URI**: The S3 URI where the Iceberg table data will be stored (e.g., `s3://your-bucket/warehouse/`).
- **AWS_ACCESS_KEY_ID**: Your AWS Access Key ID.
- **AWS_SECRET_ACCESS_KEY**: Your AWS Secret Access Key.
- **AWS_DEFAULT_REGION**: The AWS region where your S3 bucket and AWS Glue catalog are located (e.g., `eu-north-1`).

Create a `.env` file in the project root or set these environment variables in your system.

**Example `.env` file:**

```dotenv
input=your_input_topic
basic_auth_password=<some_random_password>
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
