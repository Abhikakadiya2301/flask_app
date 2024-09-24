FROM python:3.9-slim

WORKDIR /flask_app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV GOOGLE_APPLICATION_CREDENTIALS=/app/abiding-ion-436022-b5-e533269739bc.json

EXPOSE 8081
CMD ["python", "app.py"]