from flask import Flask, request, render_template
from google.cloud import storage
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import logging
from datetime import datetime

# Load environment variables and set up logging
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask app configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mssql+pyodbc://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}?"
    "driver=ODBC+Driver+17+for+SQL+Server"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# GCS configuration
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'abiding-ion-436022-b5-e533269739bc.json'
BUCKET_NAME = 'storageforapp'


def test_db_connection():
    try:
        result = db.session.execute(text('SELECT 1')).scalar()
        return result == 1
    except SQLAlchemyError as e:
        logger.error(f"Database error occurred: {str(e)}")
        return False
    finally:
        db.session.close()


def insert_file_info(filename, gcs_url):
    try:
        query = text("""
            INSERT INTO FileUploads (FileName, GCSUrl, UploadDate)
            VALUES (:filename, :gcs_url, :upload_date)
        """)
        db.session.execute(query, {
            'filename': filename,
            'gcs_url': gcs_url,
            'upload_date': datetime.utcnow()
        })
        db.session.commit()
        logger.info(f"File info inserted into database: {filename}")
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Error inserting file info into database: {str(e)}")
        return False


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file:
            try:
                # Upload file to GCS
                storage_client = storage.Client()
                bucket = storage_client.bucket(BUCKET_NAME)
                blob = bucket.blob(file.filename)
                blob.upload_from_string(file.read(), content_type=file.content_type)
                gcs_url = f"gs://{BUCKET_NAME}/{file.filename}"

                # Insert file info into database
                if test_db_connection() and insert_file_info(file.filename, gcs_url):
                    return f'File {file.filename} uploaded to GCS and info inserted into database.'
                else:
                    return f'File {file.filename} uploaded to GCS, but database operation failed.'
            except Exception as e:
                logger.error(f"Error during file upload or database insertion: {str(e)}")
                return f'Error occurred: {str(e)}'
    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)