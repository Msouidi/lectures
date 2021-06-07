import string
from pyspark import SparkContext
from pyspark.streaming import StreamingContext

# Create a local StreamingContext with two working thread and batch interval of 1 second
sc = SparkContext("local[2]", "NetworkWordCount")
sc.setLogLevel("ERROR")
ssc = StreamingContext(sc, 10)
ssc.checkpoint('.')

# Create a DStream that will connect to hostname:port, like localhost:9999
lines = ssc.socketTextStream("192.168.33.10", 9999)

# Split each line into words
words = lines.flatMap(lambda s: s.split())\
    .map(lambda e: e.strip(string.punctuation)) \
    .map(lambda s: s.lower())

# Count each word in each batch
pairs = words.map(lambda word: (word, 1))
# wordCounts = pairs.reduceByKey(lambda x, y: x + y)
wordCounts = pairs.reduceByKeyAndWindow(lambda x, y: x + y, lambda x, y: x - y, 30, 10)

# Print the first ten elements of each RDD generated in this DStream to the console
wordCounts.pprint()
#wordCounts.saveAsTextFiles()

ssc.start()             # Start the computation
ssc.awaitTermination()  # Wait for the computation to terminate