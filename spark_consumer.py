from kafka import KafkaConsumer
import json
import time
import pandas as pd
from collections import defaultdict

# Create Kafka consumer
consumer = KafkaConsumer(
    'test-topic',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Starting Kafka consumer... Waiting for messages")

# Initialize data structures for analytics
action_counts = defaultdict(int)
action_totals = defaultdict(float)
action_averages = {}
recent_transactions = []
MAX_RECENT_TRANSACTIONS = 10

# Process messages in a loop
try:
    while True:
        # Poll for messages with a timeout
        message_batch = consumer.poll(timeout_ms=1000)
        
        if not message_batch:
            print("No new messages. Waiting...")
            time.sleep(1)
            continue
            
        # Process the messages
        for topic_partition, messages in message_batch.items():
            for message in messages:
                data = message.value
                print(f"Received: {data}")
                
                # Update analytics
                action = data['action']
                price = data['price']
                
                action_counts[action] += 1
                action_totals[action] += price
                
                # Keep a list of recent transactions
                recent_transactions.append(data)
                if len(recent_transactions) > MAX_RECENT_TRANSACTIONS:
                    recent_transactions.pop(0)
                
                # Calculate averages
                for act in action_counts:
                    action_averages[act] = action_totals[act] / action_counts[act]
                
                # Print analytics every 5 messages
                if sum(action_counts.values()) % 5 == 0:
                    print("\n===== ANALYTICS =====")
                    print(f"Total events processed: {sum(action_counts.values())}")
                    print("\nAction Counts:")
                    for act, count in action_counts.items():
                        print(f"  {act}: {count}")
                    
                    print("\nAverage Price by Action:")
                    for act, avg in action_averages.items():
                        print(f"  {act}: ${avg:.2f}")
                    
                    # Create a window of the last minute if you have enough data
                    if len(recent_transactions) >= 2:
                        df = pd.DataFrame(recent_transactions)
                        df['timestamp'] = pd.to_datetime(df['timestamp'])
                        last_minute = df[df['timestamp'] > (pd.Timestamp.now() - pd.Timedelta(minutes=1))]
                        
                        if not last_minute.empty:
                            print("\nLast Minute Activity:")
                            print(f"  Events: {len(last_minute)}")
                            if 'action' in last_minute.columns:
                                print("  Actions breakdown:")
                                print(last_minute['action'].value_counts().to_dict())
                    
                    print("=====================\n")

except KeyboardInterrupt:
    print("Shutting down consumer...")
    consumer.close()