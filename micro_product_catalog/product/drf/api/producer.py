import os
import pika
import json

with open(os.path.join(os.getcwd(), 'param.txt')) as p:
    param = json.load(p)
host = param["rabbitmq"]

params = pika.URLParameters(host)

# create connection
connection = pika.BlockingConnection(params)

# create channel
channel = connection.channel()

# declare queue where to receive event
channel.queue_declare(queue='product_worker') 

def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(
        exchange='',
        routing_key='product_worker', # channel queue where to send event
        body=json.dumps(body), 
        properties=properties)
