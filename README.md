# Demo Real Time Pipeline
This application ingests real time data (synthetically generated) into Kafka Topic. A spark consumer then consumes this data, does transformations on it and displays the result
on console

# Prerequisites

* Java 8 or higher installed (required for Kafka and Spark)
* Python 3.6+ (for PySpark)
* Minimum 8GB RAM
* Administrator access on your Windows laptop

# Setup Instructions
Set Up Kafka

* Download Kafka:
Go to the Apache Kafka downloads page
Download the latest stable release (e.g., kafka_2.13-3.4.0.tgz)

* Extract Kafka:
Extract the downloaded file to a location like C:\kafka
Open the config folder and locate server.properties
Change log.dirs=/tmp/kafka-logs to log.dirs=C:/kafka/kafka-logs

* Start Zookeeper (Kafka's coordination service):

Open Command Prompt as administrator
Navigate to Kafka directory: cd C:\kafka
Run: .\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties

* Start Kafka Server (in a new Command Prompt window):
Run: .\bin\windows\kafka-server-start.bat .\config\server.properties

* Create a Topic (in a third Command Prompt window):
Run: .\bin\windows\kafka-topics.bat --create --topic test-topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

Install Apache Spark

* Download Spark:
Go to the Apache Spark downloads page
Download the latest Spark release with pre-built for Hadoop

* Extract Spark:
Extract to a location like C:\spark
Add C:\spark\bin to your Windows PATH environment variable

* Install PySpark:
Run: pip install pyspark kafka-python

# Run Instructions
Make sure Kafka is running (Zookeeper and Kafka Server)

Run the Data Producer:
Open a new Command Prompt
Run: <mark>python data_producer.py</mark>

Run the Spark Consumer:
Open another Command Prompt
<mark>Run: python spark_consumer.py</mark>

Watch the Results:
The producer will generate random e-commerce events
Spark will process these events and show average prices by action in 1-minute windows
