from kafka import KafkaProducer
import json
import time
import random
from datetime import datetime

# Create Kafka producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Generate sample data
def generate_data():
    return {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'user_id': random.randint(1, 1000),
        'action': random.choice(['click', 'view', 'purchase']),
        'product_id': random.randint(1, 100),
        'price': round(random.uniform(10, 1000), 2)
    }

# Send data to Kafka
while True:
    data = generate_data()
    producer.send('test-topic', data)
    print(f"Sent: {data}")
    time.sleep(1)  # Send a message every second