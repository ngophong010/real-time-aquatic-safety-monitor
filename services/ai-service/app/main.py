from fastapi import FastAPI, status
from pydantic import BaseModel
from kafka import KafkaProducer
import json
import os

# --- Kafka Producer Setup ---
KAFKA_BROKER_URL = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
DETECTION_TOPIC = "detection-events"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER_URL,
    value_serializer=lambda v: json.dumps(v).encode('utf-8') # Serialize JSON to bytes
)

app = FastAPI(title="Drowning Detection AI Service")

class StreamAnalysisRequest(BaseModel):
    camera_id: str
    stream_url: str

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "AI Service is running"}

@app.post("/analyze")
def analyze_stream(request: StreamAnalysisRequest):
    """
    Receives a stream URL and performs AI analysis.
    In a real-world scenario, this is where you would use OpenCV to
    process the video stream and run it through your ML model.
    """
    print(f"Analyzing stream for camera: {request.camera_id} at {request.stream_url}")
    
    if drowning_detected:
        print(f"!!! DROWNING DETECTED for camera {request.camera_id} - publishing to Kafka !!!")
        event_data = {
            "camera_id": request.camera_id,
            "confidence": highest_confidence,
            "stream_url": request.stream_url
            # Add a timestamp here
        }
        # Publish the event to the 'detection-events' topic
        producer.send(DETECTION_TOPIC, value=event_data)
        producer.flush() # Ensure message is sent
    
    # The endpoint can still return a simple confirmation
    return {"status": "analysis_complete", "detected": drowning_detected}
