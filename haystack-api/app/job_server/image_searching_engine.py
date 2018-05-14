# -*- coding:utf-8 -*-

import os
import sys
sys.path.append('..' + os.path.sep)

from api.google.google_vision_api import get_web_urls_and_images
from conf import config
from db.db_operations import get_product, add_site, finish_product_searching
import json
import logging
import pika
import requests
import timeit


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)-12s %(levelname)-8s %(message)s',
                    datefmt='%H:%M:%S',
                    filename=os.path.join(config.LOG_FILE_DIR, config.LOG_FILE_NAME),
                    filemode='a')
LOGGER = logging.getLogger(__name__)


# establish a connection with RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.MQ_CONNECTION_HOST,
                                                               heartbeat=0,
                                                               connection_attempts=3))
channel = connection.channel()
channel.queue_declare(queue=config.MQ_TASK_QUEUE, durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    request_msg = json.loads(body)
    request_url = config.WEB_SERVER_URL + '/api/image?id=' + request_msg.get('product_id')
    response = requests.request('GET', request_url)
    if 'image/' in response.headers.get('Content-Type'):
        save_path = os.path.join(config.GOOGLE_VISION_DIR,
                                 request_msg.get('product_id') + '.' + response.headers.get('Content-Type')[6:])
        # save image
        with open(save_path, 'wb') as f:
            f.write(response.content)

        # call google vision api
        image_urls, page_urls = get_web_urls_and_images(image_path=save_path, max_urls=request_msg.get('max_return'))
        # searching finished
        finish_product_searching(request_msg.get('product_id'))

        # push to MQ
        next_connection = pika.BlockingConnection(pika.ConnectionParameters(config.MQ_CONNECTION_HOST,
                                                                            heartbeat=0,
                                                                            connection_attempts=3
                                                                            ))
        next_channel = connection.channel()
        next_channel.queue_declare(queue=config.MQ_QUEUE_1ST, durable=True)

        for url in page_urls:
            site_id = add_site(request_msg.get('product_id'), url)
            message = json.dumps({
                'site_id': site_id,
                'product_id': request_msg.get('product_id'),
                'url': url,
                'image_urls': image_urls,
                'retry_times': 0,
                'debug_info': {
                    'time_cost': {
                        'crawl': 0,
                        'microdata': 0,
                        'url_pattern': 0,
                        'tag_pattern': 0,
                        'ml': 0,
                        'screenshot': 0
                    }
                }
            })
            next_channel.basic_publish(exchange='',
                                       routing_key=config.MQ_QUEUE_1ST,
                                       body=message,
                                       properties=pika.BasicProperties(
                                           delivery_mode=2,
                                       ))
            next_connection.close()

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue=config.MQ_TASK_QUEUE)

channel.start_consuming()
