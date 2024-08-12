"""
Streaming data consumer
"""
from confluent_kafka import Consumer, KafkaException, KafkaError
from datetime import datetime
import mysql.connector

TOPIC = 'set_your_topic_here'
DATABASE = 'tolldata'
USERNAME = 'root'
PASSWORD = 'root'


def create_db_connection():
    """Create and return a connection to the MySQL database."""
    print("Connecting to the database")
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port=3306,
            database=DATABASE,
            user=USERNAME,
            password=PASSWORD
        )
        print("Connected to database")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        raise


def create_kafka_consumer():
    """Create and return a Kafka consumer."""
    print("Connecting to Kafka")
    conf = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'my-group',  # Change this to a meaningful group ID
        'auto.offset.reset': 'earliest'
    }
    consumer = Consumer(conf)
    consumer.subscribe([TOPIC])
    print("Connected to Kafka")
    return consumer

def main():
    connection = create_db_connection()
    cursor = connection.cursor()
    consumer = create_kafka_consumer()

    print(f"Reading messages from the topic {TOPIC}")
    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    print(f"Reached end of partition: {msg.error()}")
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                # Extract information from Kafka message
                message = msg.value().decode("utf-8")
                timestamp, vehcile_id, vehicle_type, plaza_id = message.split(",")
                message = f"{timestamp},{vehcile_id},{vehicle_type},{plaza_id}"
                print(f"A {vehicle_type} has passed by the toll plaza {plaza_id} at {timestamp}.")
    
                # Transform the date format to suit the database schema
                dateobj = datetime.strptime(timestamp, '%a %b %d %H:%M:%S %Y')
                timestamp = dateobj.strftime("%Y-%m-%d %H:%M:%S")

                # Loading data into the database table
                sql = "INSERT INTO livetolldata (timestamp, vehicle_id, vehicle_type, toll_plaza_id) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (timestamp, vehcile_id, vehicle_type, plaza_id))
                connection.commit()
                print(f"A {vehicle_type} was inserted into the database")

    except KeyboardInterrupt:
        print("Aborted by user")
    finally:
        # Clean up
        consumer.close()
        cursor.close()
        connection.close()

if __name__ == "__main__":
    main()