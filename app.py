from flask import Flask, request, render_template
from google.cloud import storage
import os,pyodbc

app = Flask(__name__)


connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={os.getenv('DB_HOST')};"
    f"DATABASE={os.getenv('DB_NAME')};"
    f"UID={os.getenv('DB_USER')};"
    f"PWD={os.getenv('DB_PASSWORD')};"
    "Trusted_Connection=no;"
    "Encrypt=yes;"
)

conn = pyodbc.connect(connection_string)

# Configure this to your GCP project and bucket
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'abiding-ion-436022-b5-e533269739bc.json'
BUCKET_NAME = 'storageforapp'

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file:
            # Create a Cloud Storage client
            storage_client = storage.Client()

            # Get the bucket
            bucket = storage_client.get_bucket(BUCKET_NAME)

            # Create a new blob and upload the file's content
            blob = bucket.blob(file.filename)
            blob.upload_from_string(
                file.read(),
                content_type=file.content_type
            )

            return f'File {file.filename} uploaded to {BUCKET_NAME}.'
    return render_template('upload.html')

#if __name__ == '__main__':
    #app.run(debug=True, host='0.0.0.0', port=5000)