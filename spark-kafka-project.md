# Project

### Create the following project
------------    -------    -----------------    -----------    -----------------
|Python App| -> |Kafka| -> |Spark Stremaing| -> | MySql DB| -> |Apache Superset|
------------    -------    -----------------    -----------    -----------------
Python App Send data to Kafka Cluster
Kafka broker
Spark Streaming: Analyse the data

### Configure spark to listen to kafka Cluster
1. Unset the following env variable
```
unset PYSPARK_DRIVER_PYTHON
```
2. Download the following [JAR](https://mvnrepository.com/artifact/org.apache.spark/spark-streaming-kafka-0-8-assembly_2.11/2.4.7)
```
wget https://repo1.maven.org/maven2/org/apache/spark/spark-streaming-kafka-0-8-assembly_2.11/2.4.7/spark-streaming-kafka-0-8-assembly_2.11-2.4.7.jar
```
3. Start the streaming App
```
spark-submit --jars spark-streaming-kafka-0-8-assembly_2.11-2.4.7.jar app.py
```
