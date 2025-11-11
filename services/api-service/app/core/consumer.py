import json
from kafka import KafkaConsumer
from app import crud
import os

KAFKA_BROKER_URL = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
DETECTION_TOPIC = "detection-events"

async def consume_detection_events():
    consumer = KafkaConsumer(
        DETECTION_TOPIC,
        bootstrap_servers=KAFKA_BROKER_URL,
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        group_id="api-service-consumers"
    )
    print("Starting detection event consumer...")
    for message in consumer:
        event_data = message.value
        print(f"API service consumed event: {event_data}")
        # Create an alert in the database
        await crud.crud_alert.create(
            camera_id=event_data.get("camera_id"),
            confidence=event_data.get("confidence")
        )
        # In a real app, you would then produce a new event to the `alert-notifications` topic here.
