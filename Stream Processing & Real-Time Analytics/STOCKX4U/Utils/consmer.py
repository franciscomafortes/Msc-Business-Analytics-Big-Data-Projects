import ast
import datetime
from kafka import KafkaConsumer
from Stock_data import download_history
import sys
from option_parser import OptParser
from settings import bootstrap_servers, default_option

from influxdb import InfluxDBClient
client = InfluxDBClient(host='localhost', port=8086)
client.switch_database('stockdatabase')

def main():
    pass


if __name__ == "__main__":
    kwargs = OptParser.parseopts()
    print(kwargs)
    if kwargs['topic']:
        topic = kwargs['topic']
    elif kwargs['option']:
        topic = kwargs['option']
    else:
        topic = default_option

    c = KafkaConsumer(topic,
                     bootstrap_servers=bootstrap_servers,
                     auto_offset_reset='earliest',
                     enable_auto_commit=True,
                     value_deserializer=lambda x: x.decode('utf-8')
                     )

    if kwargs['counsumer_destination'] == 'influx':
        for message in c:
            sd = ast.literal_eval(message.value)
            data = {"measurement": topic,
                    "fields": sd,
                    "time" : sd["Date"]
                   }
            client.write_points([data])
    elif kwargs['counsumer_destination'] == 'file':
        pass
    else:
        for message in c:
            print(message.value)