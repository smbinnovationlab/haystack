# -*- coding:utf-8 -*-

import os
import sys
sys.path.append('..' + os.path.sep)

from analyzer import product_price_analyzer_3rd
from conf import config
from db.db_operations import add_site, set_site_finished
import json
import logging
import pika
import requests


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
channel.queue_declare(queue=config.MQ_QUEUE_3RD, durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    request_msg = json.loads(body)
    request_msg['debug_info']['time_cost']['tag_pattern'] = float(
        request_msg.get('debug_info').get('time_cost').get('tag_pattern')
    )
    request_msg['debug_info']['time_cost']['ml'] = float(
        request_msg.get('debug_info').get('time_cost').get('ml')
    )
    request_msg['debug_info']['time_cost']['screenshot'] = float(
        request_msg.get('debug_info').get('time_cost').get('screenshot')
    )

    if int(request_msg.get('retry_times')) < 3:
        try:
            ret_flag, t1, t2, t3 = product_price_analyzer_3rd.get_price(site_id=request_msg.get('site_id'),
                                                                        site_data=request_msg,
                                                                        need_screenshot=False)

            request_msg['debug_info']['time_cost']['tag_pattern'] += t1
            request_msg['debug_info']['time_cost']['ml'] += t2
            request_msg['debug_info']['time_cost']['screenshot'] += t3

            if ret_flag == -1:
                request_msg['retry_times'] += 1
                redeliver_message(request_msg)
            elif ret_flag == 0:
                # do nothing
                set_site_finished(request_msg.get('site_id'), request_msg.get('debug_info'))
                LOGGER.info('[#] (%s) %s' % (request_msg.get('retry_times'), request_msg.get('url'),))
                LOGGER.info('[V] Finish: price not found')
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
        LOGGER.info('[#] (%s) %s' % (request_msg.get('retry_times'), request_msg.get('url'),))
        LOGGER.info('[V] Finish: price not found')
        set_site_finished(request_msg.get('site_id'), request_msg.get('debug_info'))

    ch.basic_ack(delivery_tag=method.delivery_tag)


def redeliver_message(message):
    request_url = config.WEB_SERVER_URL + '/api/redeliver?routing=' + config.MQ_QUEUE_3RD
    request_headers = {'content-type': 'application/json'}
    requests.post(request_url, headers=request_headers, data=json.dumps(message))
    pass


channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue=config.MQ_QUEUE_3RD)

channel.start_consuming()
