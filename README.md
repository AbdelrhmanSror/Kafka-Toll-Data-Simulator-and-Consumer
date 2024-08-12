## Kafka Toll Data Simulator and Consumer

This repository provides a complete setup for simulating toll traffic data and consuming it using Apache Kafka and MySQL. The project includes scripts for setting up Kafka, MySQL, and Python environments to produce and consume streaming data related to toll transactions.

### Features

- **Kafka Setup**: Instructions to download, install, and configure Apache Kafka 3.7.0 with KRaft mode for managing metadata without ZooKeeper.
- **MySQL Setup**: Steps to set up a MySQL database in a Docker container, create a database and table to store toll data.
- **Python Environment**: Setup a Python virtual environment with necessary dependencies (`confluent-kafka` and `mysql-connector-python`).
- **Toll Traffic Simulator**: A Python script that simulates toll transactions, generating random vehicle data and sending it to a Kafka topic.
- **Streaming Data Consumer**: A Python script that consumes toll data from the Kafka topic, processes the data, and inserts it into a MySQL database.

### Getting Started

1. **Download and Extract Kafka**:
   ```bash
   wget https://downloads.apache.org/kafka/3.7.0/kafka_2.12-3.7.0.tgz
   tar -xzf kafka_2.12-3.7.0.tgz
   cd kafka_2.12-3.7.0
   ```

2. **Setup Kafka in KRaft Mode**:
   ```bash
   KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"
   bin/kafka-storage.sh format -t $KAFKA_CLUSTER_ID -c config/kraft/server.properties
   bin/kafka-server-start.sh config/kraft/server.properties
   ```

3. **Run MySQL in a Docker Container**:
   ```bash
   docker run --name mysql-container -e MYSQL_ROOT_PASSWORD=root -p 3306:3306 -d mysql:latest
   ```

4. **Database Setup**:
   - Download MySQL Workbench if desired to manage the MySQL server.
   - Create the `tolldata` database and `livetolldata` table:
     ```sql
     CREATE DATABASE tolldata;
     USE tolldata;
     CREATE TABLE livetolldata (
         timestamp DATETIME,
         vehicle_id INT,
         vehicle_type CHAR(15),
         toll_plaza_id SMALLINT
     );
     ```

5. **Python Environment Setup**:
   ```bash
   python3 -m venv myenv
   source myenv/bin/activate
   pip install confluent-kafka
   pip3 install mysql-connector-python
   ```

6. **Run the Toll Traffic Simulator**:
   - This script simulates toll transactions and sends data to the Kafka topic.
   - Update the Kafka topic in the script before running.
   ```python
   # python3 path/to/your/toll_traffic_simulator.py
   ```

7. **Run the Streaming Data Consumer**:
   - This script consumes data from the Kafka topic and inserts it into the MySQL database.
   - Update the Kafka topic and MySQL credentials in the script before running.
   ```python
   # python3 path/to/your/streaming_data_consumer.py
   ```

### Use Cases

- **Data Simulation**: Generate realistic toll transaction data for testing and development purposes.
- **Real-Time Data Processing**: Demonstrate the integration of Kafka with MySQL for real-time data ingestion and processing.
- **Kafka Learning**: A hands-on project to learn how to set up and work with Kafka, MySQL, and Python.

### Requirements

- Apache Kafka 3.7.0
- MySQL 8.x (running in a Docker container)
- Python 3.x with `confluent-kafka` and `mysql-connector-python` installed
