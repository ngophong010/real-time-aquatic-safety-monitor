from kafka import KafkaConsumer
import json
import os

KAFKA_BROKER_URL = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
ALERT_TOPIC = "alert-notifications" # Listening to the confirmed alerts

def send_sms(message):
    print(f"--- SENDING SMS ---")
    print(f"To: +1234567890")
    print(f"Body: {message}")
    print(f"---------------------")
    # In a real app, you'd use Twilio's library here.

consumer = KafkaConsumer(
    ALERT_TOPIC,
    bootstrap_servers=KAFKA_BROKER_URL,
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    group_id="sms-service-group" # A unique group ID
)

print("Starting SMS service consumer...")
for message in consumer:
    send_sms(message.value)
