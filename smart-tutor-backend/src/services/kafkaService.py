import json
from aiokafka import AIOKafkaProducer

producer = None

async def get_producer():
    global producer
    if not producer:
        producer = AIOKafkaProducer(
            bootstrap_servers="localhost:9092",
            value_serializer=lambda m: json.dumps(m).encode("utf-8")
        )
        await producer.start()
    return producer

async def emit_event(topic: str, payload: dict):
    producer = await get_producer()
    await producer.send_and_wait(topic, value=payload)
