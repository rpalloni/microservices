import pika
import json

from django.core.management.base import BaseCommand, CommandError
from api.models import Product, Catalog

class Command(BaseCommand):
    help = 'consumer'

    def handle(self, *args, **options):
        with open('param.txt') as p:
            param = json.load(p)

        host = param["rabbitmq"]

        params = pika.URLParameters(host)

        connection = pika.BlockingConnection(params)

        channel = connection.channel()

        channel.queue_declare(queue='product_worker') # queue where to receive event

        def callback(ch, method, properties, body):
            print('Receiving...')
            data = json.loads(body)
            print(data)

            if properties.content_type == 'product_created':
                catalog = Catalog(ct_id=data['pr_catal'])
                product = Product(pr_id=data['pr_id'], pr_catal=catalog)
                product.save()
                print('Product created!')


        channel.basic_consume(queue='product_worker', on_message_callback=callback, auto_ack=True)

        print('Start consuming...')
        channel.start_consuming()
        channel.close()