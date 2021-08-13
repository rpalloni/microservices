import pika
import json

from django.core.management.base import BaseCommand, CommandError
from api.models import Product, Catalog

class Command(BaseCommand):
    help = 'custom django command to run consumer.py'

    def handle(self, *args, **options):
        with open('param.txt') as p:
            param = json.load(p)

        host = param["rabbitmq"]

        params = pika.URLParameters(host)

        # create connection
        connection = pika.BlockingConnection(params)

        # create channel
        channel = connection.channel()

        # declare queue where to receive event
        channel.queue_declare(queue='product_worker') 

        # callback: async function called each time a new msg is added to the queue
        def callback(channel, method, properties, body):
            print('Receiving...')
            data = json.loads(body)
            print(data)

            if properties.content_type == 'product_created':
                catalog = Catalog(ct_id=data['pr_catal'])
                product = Product(pr_id=data['pr_id'], pr_catal=catalog)
                product.save()
                print('Product created!')

        # consume queue msg
        channel.basic_consume(queue='product_worker', on_message_callback=callback, auto_ack=True) # no acknowledge

        print('Start consuming...')
        channel.start_consuming() # invoke callback at each new msg

        # once msg are consumed, consumer goes back to listening