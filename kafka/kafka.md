# Kafka

### 1. Setup the local machine
```
$ sudo apt update
$ sudo apt install openjdk-8-jdk
```

### 2. Download Kafka
[Download](https://www.apache.org/dyn/closer.cgi?path=/kafka/2.8.0/kafka_2.13-2.8.0.tgz) the latest Kafka release and extract it: 
```
$ tar -xzf kafka_2.13-2.8.0.tgz
$ cd kafka_2.13-2.8.0
```

### 3. Start the kafka environment
Edit the config/server.properties and setup the external IP
```
$ vi config/server.properties
listeners=PLAINTEXT://192.168.33.13:9092
```
Run the following commands in order to start all services in the correct order: 
```
# Start the ZooKeeper service
kafka/bin/zookeeper-server-start.sh config/zookeeper.properties
```
Open another terminal session and run: 
```
# Start the Kafka broker service
kafka/bin/kafka-server-start.sh config/server.properties
```

### 4. Create a topic to store your events
 Kafka is a distributed event streaming platform that lets you read, write, store, and process events (also called records or messages in the documentation) across many machines.

Example events are payment transactions, geolocation updates from mobile phones, shipping orders, sensor measurements from IoT devices or medical equipment, and much more. These events are organized and stored in topics. Very simplified, a topic is similar to a folder in a filesystem, and the events are the files in that folder.

So before you can write your first events, you must create a topic. Open another terminal session and run: 
```
kafka/bin/kafka-topics.sh --create --topic quickstart-events --bootstrap-server 192.168.33.13:9092
```

All of Kafka's command line tools have additional options: run the kafka-topics.sh command without any arguments to display usage information. For example, it can also show you details such as the partition count of the new topic: 

```
$ bin/kafka-topics.sh --describe --topic quickstart-events --bootstrap-server 192.168.33.13:9092
Topic:quickstart-events  PartitionCount:1    ReplicationFactor:1 Configs:
    Topic: quickstart-events Partition: 0    Leader: 0   Replicas: 0 Isr: 0
```

### 5. Write some events into the topic
 A Kafka client communicates with the Kafka brokers via the network for writing (or reading) events. Once received, the brokers will store the events in a durable and fault-tolerant manner for as long as you need—even forever.

Run the console producer client to write a few events into your topic. By default, each line you enter will result in a separate event being written to the topic.

```
kafka/bin/kafka-console-producer.sh --topic quickstart-events --bootstrap-server 192.168.33.13:9092
```
You can stop the producer client with Ctrl-C at any time.

Write events as Key:Value
```
kafka/bin/kafka-console-producer.sh --topic topic1 --bootstrap-server 192.168.33.13:9092 --property "parse.key=true" --property "key.separator=:"
```

### 6. Read the events
Open another terminal session and run the console consumer client to read the events you just created:
```
kafka/bin/kafka-console-consumer.sh --topic quickstart-events --from-beginning --bootstrap-server 192.168.33.13:9092
```
You can stop the consumer client with Ctrl-C at any time.

Feel free to experiment: for example, switch back to your producer terminal (previous step) to write additional events, and see how the events immediately show up in your consumer terminal.

Because events are durably stored in Kafka, they can be read as many times and by as many consumers as you want. You can easily verify this by opening yet another terminal session and re-running the previous command again.