# Flask Application for File Upload to GCP

## Overview

This Flask application lets users upload files to a Google Cloud Platform (GCP) bucket. Upon a successful upload, the application records file information in a SQL Server database and publishes an insertion message using Google Cloud Pub/Sub. Both the front-end and back-end components of the application are deployed on Kubernetes, utilizing Docker for containerization.

## Features

- **File Upload:** Users can upload files via a web interface.
- **GCP Integration:** Uploaded files are stored in a GCP bucket.
- **Database Storage:** Metadata of the uploaded files is inserted into a SQL Server database.
- **Pub/Sub Messaging:** An insertion message is published to a Google Cloud Pub/Sub topic after each successful upload.
- **Kubernetes Deployment:** Both front-end and back-end services are containerized and deployed on Kubernetes.

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.x
- Flask
- Docker
- Kubernetes
- Google Cloud SDK
- SQL Server

## Installation

1. **Clone the repository:**

   ```bash
   git clone (https://github.com/Abhikakadiya2301/flask_app.git)
   cd (https://github.com/Abhikakadiya2301/flask_app.git)

2. **Set up a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Install dependencies:**
   ```bash
     pip install -r requirements.txt

4. **Configure environment variables:**
   ```bash
    GCP_BUCKET=<your-gcp-bucket-name>
    SQL_SERVER_CONNECTION_STRING=<your-sql-server-connection-string>
    PUBSUB_TOPIC=<your-pubsub-topic-name>

***Run the Application***
```bash 
export FLASK_APP=app.py
export FLASK_ENV=development
flask run

**Testing The Feature**
1. Navigate to http://localhost:5000 in your web browser.
2. Use the file upload interface to select and upload a file.
