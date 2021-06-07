from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

sc = SparkContext(appName="PythonSparkStreamingKafka")
sc.setLogLevel("WARN")

ssc = StreamingContext(sc, 10)
directKafkaStream = KafkaUtils.createDirectStream(ssc, ["topic1"], {"metadata.broker.list": "192.168.33.11:9092"})

directKafkaStream.pprint()

#Starting Spark context
ssc.start()
ssc.awaitTermination()