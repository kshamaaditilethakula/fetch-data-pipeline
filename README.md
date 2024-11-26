# Kafka Stream Processor for User Login Data

This project implements a Kafka-based stream processing system for analyzing user login data in real-time. It consists of a Kafka consumer that processes incoming messages, performs data validation and transformation, and provides insights on user behavior and app usage.

## Project Structure

- `consumer.py`: Main Python script containing the Kafka consumer and stream processing logic.
- `docker-compose.yml`: Docker Compose file for setting up the Kafka environment.
- `requirements.txt`: List of Python dependencies required for the project.

## Prerequisites

- Python 3.6 or higher
- Docker and Docker Compose
- pip (Python package installer)

## Setup and Installation

1. Clone the repository and navigate to the project directory.

2. Create a Python virtual environment:

```bash
python3 -m venv venv
```

3. Activate the virtual environment:

- On macOS and Linux:
  ```bash
  source venv/bin/activate
  ```
- On Windows:
  ```bash
  venv\Scripts\activate
  ```

4. Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

5. Start the Kafka environment using Docker Compose:

```bash
docker compose up -d
```

This command will set up Zookeeper, Kafka broker, and a Python producer for generating sample data.

## Running the Kafka Consumer

After setting up the environment, you can start the Kafka consumer by navigating into consumer directory:

```bash
cd consumer
```

```bash
python3 consumer.py
```

This will initiate the `KafkaStreamProcessor` class, which will:
- Consume messages from the 'user-login' topic
- Process and validate the data
- Send processed data to the 'processed-user-login' topic
- Print real-time insights every 100 messages processed

## Features

- Real-time processing of user login events
- Data validation and transformation
- IP address masking for privacy
- Device type normalization
- App version categorization
- Comprehensive analytics and insights

## Design Choices and Data Flow

### Architecture

The system consists of three main components:

1. Kafka Cluster: Includes Zookeeper and Kafka broker
2. Python Producer: Generates sample user login data
3. Python Consumer: Processes and analyzes the login data

### Data Flow

1. The Python producer generates user login events and sends them to the 'user-login' Kafka topic.
2. The `KafkaStreamProcessor` consumes messages from the 'user-login' topic.
3. Each message is validated, transformed, and enriched with additional data.
4. Processed messages are sent to the 'processed-user-login' topic.
5. Real-time insights are generated and printed periodically.

## Efficiency and Scalability

- Efficient data processing through single-pass validation and transformation
- Use of `defaultdict` for efficient metric tracking
- Leverages Kafka's partitioning capabilities for horizontal scaling
- Docker-based setup for easy deployment and scaling

## Fault Tolerance

- Consumer group implementation for automatic work redistribution
- Auto-commit for regular offset updates
- Producer configured with `acks='all'` for message replication
- Comprehensive error handling throughout the code
- Kafka cluster can be configured with higher replication factor for production

## Monitoring and Insights

The system provides real-time insights on:
- User engagement metrics
- Platform analytics
- App version adoption
- Geographic distribution
- Data quality summary

## Extensibility

- Modular design of `KafkaStreamProcessor` for easy addition of new features
- Docker Compose setup can be extended for additional services or monitoring tools

## Kafka Environment

The `docker-compose.yml` file sets up the following services:

- Zookeeper (accessible on port 22182)
- Kafka broker (accessible on localhost:29092)
- Python producer (for generating sample data)

## Troubleshooting

- If you encounter issues connecting to Kafka, ensure that the Docker containers are running:
  ```bash
  docker-compose ps
  ```
- Check the logs of the Kafka and Zookeeper containers:
  ```bash
  docker-compose logs kafka zookeeper
  ```
- Verify that the Kafka broker is accessible on localhost:29092

## Dependencies

- kafka-python 2.0.2
- ipaddress 1.0.23

These dependencies are listed in the `requirements.txt` file and will be installed during the setup process.