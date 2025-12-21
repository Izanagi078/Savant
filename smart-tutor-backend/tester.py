from aiokafka import AIOKafkaProducer
import asyncio

async def send_message():
    producer = AIOKafkaProducer(bootstrap_servers='localhost:9092')
    await producer.start()
    try:
        await producer.send_and_wait("user_prompt", b"Hello from Arman!")
    finally:
        await producer.stop()

asyncio.run(send_message())
