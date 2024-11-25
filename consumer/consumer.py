from kafka import KafkaConsumer, KafkaProducer
import json
import datetime

# Define Kafka Consumer to read messages from 'user-login' topic
consumer = KafkaConsumer(
    'user-login',
    bootstrap_servers='localhost:29092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Define Kafka Producer to send processed data to 'user-login-processed' topic
producer = KafkaProducer(
    bootstrap_servers='localhost:29092',
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# Process messages from 'user-login' topic
for message in consumer:
    data = message.value
    # Example Processing: Add a processed timestamp
    data['processed_timestamp'] = datetime.datetime.now().isoformat()

    # Produce the processed message to a new topic
    producer.send('user-login-processed', value=data)

    # Log processed message to console for verification
    print(f"Processed message: {data}")