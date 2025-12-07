from confluent_kafka import Producer
import json

producer = Producer({"bootstrap.servers": "localhost:9092"})

def emit_event(topic: str, payload: dict):
    producer.produce(topic, key=payload.get("type", "content"), value=json.dumps(payload))
    producer.flush()
