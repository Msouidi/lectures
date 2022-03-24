import string
from pyspark.sql import SparkSession, Row
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark.sql.types import FloatType


def process(time, rdd):
    print("========= %s =========" % str(time))
    if not rdd.isEmpty():
        df = rdd.map(lambda line: Row(longitude=line[0], 
                              latitude=line[1], 
                              housingMedianAge=line[2],
                              totalRooms=line[3],
                              totalBedRooms=line[4],
                              population=line[5], 
                              households=line[6],
                              medianIncome=line[7],
                              medianHouseValue=line[8])).toDF()

        df = df.withColumn("longitude", df["longitude"].cast(FloatType())) \
           .withColumn("latitude", df["latitude"].cast(FloatType())) \
           .withColumn("housingMedianAge",df["housingMedianAge"].cast(FloatType())) \
           .withColumn("totalRooms", df["totalRooms"].cast(FloatType())) \
           .withColumn("totalBedRooms", df["totalBedRooms"].cast(FloatType())) \
           .withColumn("population", df["population"].cast(FloatType())) \
           .withColumn("households", df["households"].cast(FloatType())) \
           .withColumn("medianIncome", df["medianIncome"].cast(FloatType())) \
           .withColumn("medianHouseValue", df["medianHouseValue"].cast(FloatType()))

        df.write.format('jdbc').options(
            url='jdbc:mysql://192.168.33.10/data',
            dbtable='houses',
            user='admin',
            password='admin').mode('append').save()

spark = SparkSession.builder \
        .master("local[2]") \
        .appName("Cal_house") \
        .getOrCreate()

sc = spark.sparkContext
sc.setLogLevel("ERROR")
ssc = StreamingContext(sc, 10)

directKafkaStream = KafkaUtils.createDirectStream(ssc, ["my_topic"], {"metadata.broker.list": "192.168.33.13:9092"})

rdd = directKafkaStream.map(lambda line: line[1].split(","))
rdd.foreachRDD(process)

ssc.start()
ssc.awaitTermination()
