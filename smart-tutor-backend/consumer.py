from confluent_kafka import Consumer
import json

consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'test-group',
    'auto.offset.reset': 'earliest'
})

consumer.subscribe(['user_prompt'])

print("Listening for messages on 'user_prompt'...")

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        print("Consumer error:", msg.error())
        continue

    try:
        message = msg.value().decode('utf-8')
        print(f"Raw message: {message}")
        data = json.loads(message)

        # Example processing logic
        request_id = data.get("request_id")
        user_id = data.get("user_id")
        topic = data.get("topic")
        level = data.get("level")

        print(f"✅ Received prompt from user '{user_id}' (request ID: {request_id})")
        print(f"🎯 Topic: {topic} | Level: {level}")
        print("🚀 Generating course content...")

        # Simulate processing
        # generate_course(topic, level)  # <-- your logic here

    except json.JSONDecodeError:
        print("⚠️ Could not parse message as JSON. Raw content:")
        print(msg.value().decode('utf-8'))
    except Exception as e:
        print("❌ Error processing message:", e)
