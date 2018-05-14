# -*- coding:utf-8 -*-

import os
import sys
sys.path.append('..' + os.path.sep)

from analyzer import product_price_analyzer_1st
from conf import config
from db.db_operations import add_site, set_site_finished
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
channel.queue_declare(queue=config.MQ_QUEUE_1ST, durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    request_msg = json.loads(body)
    request_msg['debug_info']['time_cost']['crawl'] = float(
        request_msg.get('debug_info').get('time_cost').get('crawl')
    )
    request_msg['debug_info']['time_cost']['microdata'] = float(
        request_msg.get('debug_info').get('time_cost').get('microdata')
    )
    request_msg['debug_info']['time_cost']['screenshot'] = float(
        request_msg.get('debug_info').get('time_cost').get('screenshot')
    )

    if int(request_msg.get('retry_times')) < 3:
        try:
            ret_flag, t1, t2, t3 = product_price_analyzer_1st.get_price(site_id=request_msg.get('site_id'),
                                                                        site_data=request_msg,
                                                                        need_screenshot=False)

            request_msg['debug_info']['time_cost']['crawl'] += t1
            request_msg['debug_info']['time_cost']['microdata'] += t2
            request_msg['debug_info']['time_cost']['screenshot'] += t3

            if ret_flag == -1:
                request_msg['retry_times'] += 1
                redeliver_message(request_msg)
            elif ret_flag == 0:
                # push into next queue
                next_connection = pika.BlockingConnection(pika.ConnectionParameters(config.MQ_CONNECTION_HOST,
                                                                                    heartbeat=0,
                                                                                    connection_attempts=3
                                                                                    ))
                next_channel = connection.channel()
                next_channel.queue_declare(queue=config.MQ_QUEUE_2ND, durable=True)
                next_channel.basic_publish(exchange='',
                                           routing_key=config.MQ_QUEUE_2ND,
                                           body=json.dumps(request_msg),
                                           properties=pika.BasicProperties(
                                               delivery_mode=2,
                                           ))
                next_connection.close()
            else:
                set_site_finished(request_msg.get('site_id'), request_msg.get('debug_info'))
                LOGGER.info('[#] (%s) %s' % (request_msg.get('retry_times'), request_msg.get('url'),))
                LOGGER.info('[V] Finish: price found')
        except Exception as e:
            request_msg['retry_times'] += 1
            redeliver_message(request_msg)
            LOGGER.info('[#] (%s) %s' % (request_msg.get('retry_times'), request_msg.get('url'),))
            LOGGER.info('[X] Exception: %s' % (str(e),))
    else:
        set_site_finished(request_msg.get('site_id'), request_msg.get('debug_info'))
        LOGGER.info('[#] (%s) %s' % (request_msg.get('retry_times'), request_msg.get('url'),))
        LOGGER.info('[V] Finish: price not found')

    ch.basic_ack(delivery_tag=method.delivery_tag)


def redeliver_message(message):
    request_url = config.WEB_SERVER_URL + '/api/redeliver?routing=' + config.MQ_QUEUE_1ST
    request_headers = {'content-type': 'application/json'}
    try:
        requests.post(request_url, headers=request_headers, data=json.dumps(message))
    except Exception as e:
        pass


channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue=config.MQ_QUEUE_1ST)

channel.start_consuming()
