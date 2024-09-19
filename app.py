from flask import Flask, request, render_template
from google.cloud import storage
import os

app = Flask(__name__)

# Configure this to your GCP project and bucket
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'abiding-ion-436022-b5-6b79515dad55.json'
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

if __name__ == '__main__':
    app.run(debug=True)