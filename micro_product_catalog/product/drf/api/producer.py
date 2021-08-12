import os
import pika
import json

with open(os.path.join(os.getcwd(), 'param.txt')) as p:
    param = json.load(p)
host = param["rabbitmq"]

params = pika.URLParameters(host)

connection = pika.BlockingConnection(params)

channel = connection.channel()

def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(
        exchange='',
        routing_key='product_worker', # queue where to send event
        body=json.dumps(body), 
        properties=properties)