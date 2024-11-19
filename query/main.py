import os
from flask import Flask, render_template
from dotenv import load_dotenv
import pandas as pd
from requests import request
from flask import Flask, render_template, request
from flask_httpauth import HTTPBasicAuth
from pyathena import connect
import pandas as pd
import os
from werkzeug.security import generate_password_hash, check_password_hash

# Load environment variables
load_dotenv()

app = Flask(__name__)
auth = HTTPBasicAuth()

# Basic auth configuration
users = {
    "admin": generate_password_hash(os.environ["password"])  # Replace with your desired username and password
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username
    return None



# Connect to Athena
conn = connect(
    s3_staging_dir=os.environ["AWS_S3_URI"],  # Replace with your S3 bucket for Athena query results
    region_name=os.environ["AWS_DEFAULT_REGION"]
)

def query_athena(sql_query):
    # Execute the query and load the results into a Pandas DataFrame
    df = pd.read_sql(sql_query, conn)
    return df



@app.route('/', methods=['GET', 'POST'])
@auth.login_required
def index():

    if request.method == "GET":

        # Set a default code snippet if custom_code is empty (first load)
        default_code = f"""SELECT * FROM "glue"."{os.environ['table_name']}" LIMIT 100"""
        
        message = "Query data please."


        return render_template('index.html', tables=pd.DataFrame().to_html(classes='data'), titles="Query data", message=message, custom_code=default_code)

    custom_code = default_code if request.method == 'GET' else request.form.get('custom_code', '')

    try:
        
        # Load and join tables
        df = query_athena(custom_code)
        
        message = "Data loaded successfully." if df is not None else "No data found."

        # Render the result as an HTML table
        if df is not None:
            table_html = df[:500].to_html(classes='data')
        else:
            table_html = ""
    except Exception as e:
        df = None
        message = str(e)
        table_html = ""

    return render_template('index.html', tables=table_html, titles=df.columns.values if df is not None else [], message=message, custom_code=custom_code)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)