# PostgreSQL CDC transformation

This service converts PostgreSQL CDC specific messages to unified format for Iceberg sink.

## Environment variables

The code sample uses the following environment variables:

- **input**: Name of the input topic to listen to.
- **output**: Name of the output topic to write to.

