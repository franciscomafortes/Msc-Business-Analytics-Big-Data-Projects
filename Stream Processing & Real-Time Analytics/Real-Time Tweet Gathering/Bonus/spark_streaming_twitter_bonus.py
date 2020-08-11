from pyspark import SparkConf,SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import Row,SQLContext
import sys
import requests

def aggregate_tags_count(new_values, total_sum):
    return sum(new_values) + (total_sum or 0)


def h(n):
    return h % 1001


def trailing_zeroes(num):
  """Counts the number of trailing 0 bits in num."""

  if num == 0:
    return 32 # Assumes 32 bit integer inputs!
  p = 0
  while (num >> p) & 1 == 0:
    p += 1
  return p


max_tail = 0


def flajolet_martin(rdd):
    global max_tail
    
    v = rdd.take(1)
    print(v)
    if len(v) > 0:
        h = hash(v[0])
        max_tail = max(max_tail, trailing_zeroes(h))


# create spark configuration
conf = SparkConf()
conf.setAppName("TwitterStreamApp")
# create spark context with the above configuration
sc = SparkContext(conf=conf)
sc.setLogLevel("ERROR")
# create the Streaming Context from the above spark context with interval size 2 seconds
ssc = StreamingContext(sc, 2)
# setting a checkpoint to allow RDD recovery
ssc.checkpoint("Checkpoint_TwitterApp")
# read data from port 9096
dataStream = ssc.socketTextStream("localhost",9096)
# split each tweet into words
words = dataStream.flatMap(lambda line: line.split(" "))
# filter the words to get only hashtags, then map each hashtag to be a pair of (hashtag,1)
hashtags = words.filter(lambda w: '#' in w).map(lambda x: (x, 1))
# adding the count of each hashtag to its last count using updateStateByKey
tags_totals = hashtags.updateStateByKey(aggregate_tags_count)
tags_totals.pprint()
# do the processing for each RDD generated in each interval with flajolet martin function
tags_totals.foreachRDD(flajolet_martin)
# start the streaming computation
ssc.start()
# wait for the streaming to finish
ssc.awaitTermination()
