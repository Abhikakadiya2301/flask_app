from flask import Flask, request, render_template
from google.cloud import storage
import os,logging
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from datetime import datetime, timezone
from pubsub_utils import publish_message, subscribe_messages

load_dotenv()

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mssql+pyodbc://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}?"
    "driver=ODBC+Driver+17+for+SQL+Server"
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the SQLAlchemy db instance
db = SQLAlchemy(app)

def test_conn():
    try:
        logger.info("Attempting database connection...")
        result = db.session.execute(text('SELECT 1')).scalar()
        logger.info(f"Query result: {result}")
        if result == 1:
            logger.info("Database connection successful")
            return True
        else:
            logger.warning(f"Unexpected result from database: {result}")
            return False
    except SQLAlchemyError as e:
        logger.error(f"Database error occurred: {str(e)}")
        return False
    finally:
        logger.info("Closing database session")
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
            'upload_date': datetime.now(timezone.utc)
        })
        db.session.commit()
        logger.info(f"File info inserted into database: {filename}")
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Error inserting file info into database: {str(e)}")
        return False

# Configure this to your GCP project and bucket
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'abiding-ion-436022-b5-af4aafefaf70.json'
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

            gcs_url = f"gs://{BUCKET_NAME}/{file.filename}"
            # Test database connection
            db_connected = test_conn()

            if db_connected:
                # Insert file info into the database
                insert_success = insert_file_info(file.filename, gcs_url)
                if insert_success:
                    message = f"File '{file.filename}' has been uploaded to {BUCKET_NAME}"
                    publish_message(message)
                    return f'File {file.filename} uploaded to {BUCKET_NAME} and info inserted into database! Message published 1!'
                else:
                    return f'File {file.filename} uploaded to {BUCKET_NAME}, but database insertion failed.'
            else:
                return f'File {file.filename} uploaded to {BUCKET_NAME}, but database connection failed.'
    return render_template('upload.html')

# Callback function for message processing
def callback(message):
    print(f"Received message: {message.data.decode('utf-8')}")
    message.ack()  # Acknowledge message so it can be removed from the queue

# Background task to subscribe to messages
@app.before_request
def start_subscriber():
    # Start the Pub/Sub subscription thread
    from threading import Thread
    if not hasattr(app, 'subscriber_started'):
        Thread(target=subscribe_messages, args=(callback,)).start()
        app.subscriber_started = True

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)