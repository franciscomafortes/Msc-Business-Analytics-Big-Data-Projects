import datetime as dt
from kafka import KafkaProducer
from Stock_data import download_history, get_realtime
import sys
from option_parser import OptParser
from settings import bootstrap_servers
import time

def main():
    pass


if __name__ == "__main__":
    kwargs = OptParser.parseopts()
    if kwargs['destination'] == 'kafka':
        p = KafkaProducer(bootstrap_servers=bootstrap_servers,
                          value_serializer=lambda x:str(x).encode('utf-8'))

    if kwargs['source'] == 'stocks':
        if kwargs['realtime']:
            realtime_data = get_realtime(kwargs['option'])
            for data in realtime_data:
                x = {"Date" : str(dt.datetime.now()),
                     "price" : data}
                if kwargs['destination'] == 'screen':
                    print(x)
                elif kwargs['destination'] == 'kafka':
                    if kwargs['topic']:
                        print("writing to", kwargs['topic'])
                        p.send(kwargs['topic'].strip(), value = x)
                    else:
                        print("writing to", kwargs['option'])
                        p.send(kwargs['option'].strip(), value = x)
                    p.flush()
                time.sleep(60)
        data = download_history(kwargs['option'], kwargs['period'], kwargs['interval'] )

    if kwargs['destination'] == 'file':
        pass
    else:
        for d in data.itertuples():
            x = { "Open":d.Open,
                  "High":d.High,
                  "Close":d.Close,
                  "Volume":d.Volume,
                  "Low":d.Low,
                  "Date":str(d.Index)
            }
            if kwargs['destination'] == 'screen':
                print(x)
            elif kwargs['destination'] == 'kafka':
                if kwargs['topic']:
                    print("writing to", kwargs['topic'])
                    p.send(kwargs['topic'].strip(), value = x)
                else:
                    print("writing to", kwargs['option'])
                    p.send(kwargs['option'].strip(), value = x)
                p.flush()