from pyspark.sql import SparkSession, Row
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark.sql.types import FloatType, StringType
from pyspark.sql.functions import to_date


def process(time, rdd):
    if not rdd.isEmpty():
        df = rdd.map(lambda line: Row(date=line[0], 
                              number=line[1], 
                              country_code=line[2])).toDF()
        
        df = df.withColumn("date", to_date(df["date"], 'dd/MM/yyyy')) \
           .withColumn("number", df["number"].cast(FloatType())) \
           .withColumn("country_code",df["country_code"].cast(StringType()))
          
        df.write.mode('append').csv('outputs/')

                     
                     
spark = SparkSession.builder \
        .master("local[2]") \
        .appName("data") \
        .getOrCreate()

sc = spark.sparkContext
sc.setLogLevel("ERROR")
ssc = StreamingContext(sc, 10)

directKafkaStream = KafkaUtils.createDirectStream(ssc, ["my_topic"], {"metadata.broker.list": "192.168.33.13:9092"})
drdd = directKafkaStream.map(lambda x: x[1].split(','))
drdd.foreachRDD(process)


ssc.start()
ssc.awaitTermination()
