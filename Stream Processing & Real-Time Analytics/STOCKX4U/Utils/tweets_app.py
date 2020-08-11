from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from kafka import SimpleProducer, KafkaClient

ACCESS_TOKEN = '1235248071753297921-fYxuhhGVzx0cyMr7Yqo2JDWC92zim9'
ACCESS_SECRET = 'p3GjLKVtCa8BpHj16yMrOsra3plgMqxwUIyRwTKYuchcy'
CONSUMER_KEY = 'YJ45GoZQPqUx3tMH1BNTsCS4i'
CONSUMER_SECRET = 'ByloCGLiJLtmxkMEVPsjMPHcZlN4HoJcgvHOF3B0cKYMT1ZAgN'

class StdOutListener(StreamListener):
    def on_data(self, data):
        producer.send_messages("Tesla", data.encode('utf-8'))
        print (data)
        return True
    def on_error(self, status):
        print (status)

kafka = KafkaClient("localhost:9092")
producer = SimpleProducer(kafka)
l = StdOutListener()
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
stream = Stream(auth, l)
stream.filter(track=['Tesla', 'tesla', 'Elon Musk', 'Elon', 'tesla'])

