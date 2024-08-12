"""
Toll Traffic Simulator
"""
from time import sleep, time, ctime
from random import random, randint, choice
from confluent_kafka import Producer

# Kafka Producer configuration
conf = {
    'bootstrap.servers': 'localhost:9092'
}
producer = Producer(**conf)

TOPIC = 'set_your_topic_here'  # Replace with your actual Kafka topic

# Vehicle types to simulate
VEHICLE_TYPES = ("car", "car", "car", "car", "car", "car", "car", "car",
                 "car", "car", "car", "truck", "truck", "truck",
                 "truck", "van", "van")

def delivery_report(err, msg):
    """ Delivery report callback called once for each message produced. """
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

# Simulate toll traffic
for _ in range(100000):
    vehicle_id = randint(10000, 10000000)
    vehicle_type = choice(VEHICLE_TYPES)
    now = ctime(time())
    plaza_id = randint(4000, 4010)
    message = f"{now},{vehicle_id},{vehicle_type},{plaza_id}"
    print(f"A {vehicle_type} has passed by the toll plaza {plaza_id} at {now}.")
    
    # Produce the message to the Kafka topic
    producer.produce(TOPIC, value=message, callback=delivery_report)
    
    # Wait for messages to be delivered
    producer.poll(1)
    
    # Random sleep to simulate random traffic intervals
    sleep(random() * 2)

# Wait for any outstanding messages to be delivered
producer.flush()