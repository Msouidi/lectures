import string
import sys
from pyspark import SparkContext


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: wordcount <file>", file=sys.stderr)
        sys.exit(-1)

    sc = SparkContext(appName="PythonSparkStreamingKafka")

    rdd = sc.textFile(sys.argv[1])
    rdd.flatMap(lambda s: s.split()) \
        .map(lambda e: e.strip(string.punctuation)) \
        .map(lambda s: s.lower()) \
        .map(lambda mot: (mot, 1)) \
        .reduceByKey(lambda a,b: a+b) \
        .sortBy(lambda x: x[1], False) \
        .saveAsTextFile('wordCount-output')