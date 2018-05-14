# -*- coding:utf-8 -*-

import os
import sys
sys.path.append('.')

from api.google.google_vision_api import get_web_urls_and_images
from conf import config
from db.db_operations import get_product, add_site, add_product
from db.initialize_db import init_db
from flask import Flask, request, send_file
from flask_cors import CORS
import datetime
import json
import pika
import uuid


app_web_server = Flask(__name__)
CORS(app_web_server)


def clear_old_log():
    log_file_path = os.path.join(config.LOG_FILE_DIR, config.LOG_FILE_NAME)
    with open(log_file_path, 'w') as f:
        f.write('')


class DateEncoder(json.JSONEncoder):
    def default(self, o):
        return (
            o.strftime('%Y-%m-%d %H:%M:%S')
            if isinstance(o, datetime.datetime)
            else json.JSONEncoder.default(self, o)
        )


@app_web_server.route('/api/product', methods=['GET'])
def handle_get_product():
    product_id = request.args.get('id')
    product_info = get_product(product_id)
    return json.dumps(product_info, cls=DateEncoder)


@app_web_server.route('/api/product/debug', methods=['GET'])
def handle_get_product_debug():
    product_id = request.args.get('id')
    product_info = get_product(product_id, debug=True)
    return json.dumps(product_info, cls=DateEncoder)


@app_web_server.route('/api/upload', methods=['POST'])
def handle_upload():
    if request.method == 'POST':
        # clear old log
        clear_old_log()

        max_return = request.args.get('max') if request.args.get('max') else '20'

        file_in_form = False
        if request.data == b'':
            file_in_form = True

        product_id = str(uuid.uuid1())
        print(product_id)
        add_product(product_id)

        if file_in_form:
            file = request.files['file']
            image_path = os.path.join(config.PRODUCT_UPLOAD_DIR, product_id + '.' + file.filename.split('.')[1])
            file.save(image_path)
        else:
            file_name = request.headers.get('slug')
            image_path = os.path.join(config.PRODUCT_UPLOAD_DIR, product_id + '.' + file_name.split('.')[1])
            with open(image_path, 'wb') as f:
                f.write(request.data)

        # # call google vision api
        # image_urls, page_urls = get_web_urls_and_images(image_path=image_path, max_urls=max_return)
        # print(image_urls)
        # print(page_urls)

        # RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.MQ_CONNECTION_HOST,
                                                                       heartbeat=0,
                                                                       connection_attempts=3))
        channel = connection.channel()
        # channel.queue_declare(queue=config.MQ_QUEUE_1ST, durable=True)
        channel.queue_declare(queue=config.MQ_TASK_QUEUE, durable=True)
        message = json.dumps({
            'product_id': product_id,
            'max_return': max_return
        })
        channel.basic_publish(exchange='',
                              routing_key=config.MQ_TASK_QUEUE,
                              body=message,
                              properties=pika.BasicProperties(
                                  delivery_mode=2,
                              ))
        connection.close()
        return json.dumps({'id': product_id})


@app_web_server.route('/api/redeliver', methods=['POST'])
def handle_redeliver():
    routing_key = request.args.get('routing')
    data = request.get_data().decode('utf-8')

    # RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.MQ_CONNECTION_HOST,
                                                                   heartbeat=0,
                                                                   connection_attempts=3))
    channel = connection.channel()
    channel.queue_declare(queue=routing_key, durable=True)

    channel.basic_publish(exchange='',
                          routing_key=routing_key,
                          body=data,
                          properties=pika.BasicProperties(
                              delivery_mode=2,
                          ))
    connection.close()
    return 'success'


@app_web_server.route('/api/image', methods=['GET'])
def handle_get_picture():
    product_id = request.args.get('id')
    is_image_exist = False
    image_ext = None
    for root, dirs, files in os.walk(config.PRODUCT_UPLOAD_DIR):
        for f in files:
            f_name, f_ext = os.path.splitext(f)
            if f_name == product_id:
                is_image_exist = True
                image_ext = f_ext[1:]
                break
        if is_image_exist:
            break
    if is_image_exist:
        pic_path = os.path.join(config.PRODUCT_UPLOAD_DIR, product_id + '.' + image_ext)
        return send_file(pic_path, mimetype='image/' + image_ext)
    else:
        return 'fail'
