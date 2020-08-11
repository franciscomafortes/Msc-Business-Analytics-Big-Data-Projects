
# coding: utf-8

# ## 1) Importing Libraries

# In[ ]:

import socket
import sys
import requests
import requests_oauthlib 
import json


# ## 2) Access Keys
# 

# In[ ]:

ACCESS_TOKEN = '1002190093476614144-UKiIT8ItxW5SlOaOMFXSIORRs2UU86' 
ACCESS_SECRET = '52sHTHcrY7xGyGdkFBSgU3wHlmrbZkQnYEjognLWRvTbq' 
CONSUMER_KEY = 'hzFNAzjV9GUi8r3ORdP0n9ajP'
CONSUMER_SECRET = 'rOMEcVW5zhcOA0yd8sQ3k3QhVnmrqE9GCkMl324lXew3ucmXGU'


# In[ ]:

my_auth = requests_oauthlib.OAuth1(CONSUMER_KEY, CONSUMER_SECRET,ACCESS_TOKEN, ACCESS_SECRET)


# ## 3) Functions Creation

# In[ ]:

def get_tweets():
    url = 'https://stream.twitter.com/1.1/statuses/filter.json'
    query_data = [('language', 'en'), ('locations', '-130,-20,100,50'),('track','covid19')] 
    query_url = url + '?' + '&'.join([str(t[0]) + '=' + str(t[1]) for t in query_data]) 
    response = requests.get(query_url, auth=my_auth, stream=True) 
    print(query_url, response)
    return response


# In[ ]:

def send_tweets_to_spark(http_resp, tcp_connection): 
    for line in http_resp.iter_lines():
        try:
            full_tweet = json.loads(line)
            tweet_text = full_tweet['text']
            print("Tweet Text: " + tweet_text)
            print ("------------------------------------------") 
            tcp_connection.send(tweet_text + '\n')
        except:
                e = sys.exc_info()[0]
                print("Error: %s" % e)


# ## 4) Connecting to TCP

# In[ ]:

TCP_IP = "localhost"
TCP_PORT = 9096
conn = None
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
print("Waiting for TCP connection...")
conn, addr = s.accept()
print("Connected... Starting getting tweets.") 
resp = get_tweets() 
send_tweets_to_spark(resp, conn)

