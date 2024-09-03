from kafka import KafkaProducer
import csv
import json
import os

# Kafka producer configuration
producer = KafkaProducer(
    bootstrap_servers=[os.environ['KAFKA_BOOTSTRAP_SERVERS']],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Define the Kafka topic
topic = 'iot_telemetry'

# Read the CSV file and send each row as a message
with open('iot_telemetry_data.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        producer.send(topic, value=row)
        print(f"Sent: {row}")

producer.flush()
producer.close()

