from google.cloud import pubsub_v1
import os

# Project, topic, and subscription settings
project_id = os.getenv('GCP_PROJECT_ID')
topic_id = os.getenv('PUBSUB_TOPIC_ID')
subscription_id = os.getenv('PUBSUB_SUBSCRIPTION_ID')

# Initialize Publisher and Subscriber clients
publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()

# Build topic and subscription paths
topic_path = publisher.topic_path(project_id, topic_id)
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def publish_message(message):
    try:
        # Data must be in byte string format
        future = publisher.publish(topic_path, message.encode("utf-8"))
        print(f"Published message ID: {future.result()}")
    except Exception as e:
        print(f"Error publishing message: {e}")

def subscribe_messages(callback):
    try:
        # Receive messages and call the callback function on each
        future = subscriber.subscribe(subscription_path, callback)
        print(f"Listening for messages on {subscription_path}...")

        # Run the subscriber until an exception occurs or the process is stopped
        future.result()
    except Exception as e:
        print(f"Error subscribing to messages: {e}")
