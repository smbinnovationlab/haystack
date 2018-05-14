# -*- coding:utf-8 -*-

import os
import sys
sys.path.append('.')

# from api.anywhere.get_products import sync_products
from api.google.google_vision_api import handle_images
from analyzer.product_price_analyzer import get_price
from conf import config
from db.db_operations import add_to_favourites, get_events, get_product_site, get_vendor_product, get_crawled_sites
from db.db_operations import get_status, get_product_id, update_product_status, remove_from_favourites
from db.initialize_db import init_db
from flask import Flask, request, redirect, url_for, send_file
from flask_cors import CORS
import datetime
import json
import socket
import urllib.error
import urllib.parse
import urllib.request


app_web = Flask(__name__)
CORS(app_web)


class DateEncoder(json.JSONEncoder):
    def default(self, o):
        return (
            o.strftime('%Y-%m-%d %H:%M:%S')
            if isinstance(o, datetime.datetime)
            else json.JSONEncoder.default(self, o)
        )


@app_web.route('/get_events', methods=['GET'])
def handle_get_events():
    events = get_events()
    return json.dumps(events, cls=DateEncoder)


@app_web.route('/get_products', methods=['GET'])
def handle_get_products():
    products = get_vendor_product()
    return json.dumps(products, cls=DateEncoder)


@app_web.route('/get_product/<product_id>', methods=['GET'])
def handle_get_product(product_id):
    product_info = get_vendor_product(product_id)
    return json.dumps(product_info, cls=DateEncoder)


@app_web.route('/get_product_site/<product_site_id>/<event_id>', methods=['GET'])
def handle_get_product_site(product_site_id, event_id):
    product_site_info = get_product_site(product_site_id, event_id)
    return json.dumps(product_site_info, cls=DateEncoder)


@app_web.route('/add_to_favourites', methods=['POST'])
def handle_add_to_favourites():
    product_id = request.form['product_id']
    status = add_to_favourites(product_id)
    return status


@app_web.route('/remove_from_favourites', methods=['POST'])
def handle_remove_from_favourites():
    product_id = request.form['product_id']
    status = remove_from_favourites(product_id)
    return status


@app_web.route('/get_crawled_sites', methods=['GET'])
def handle_get_crawled_sites():
    crawled_sites = get_crawled_sites()
    return json.dumps(crawled_sites, cls=DateEncoder)


@app_web.route('/get_status', methods=['GET'])
def handle_get_status():
    status = get_status()
    return json.dumps(status)


@app_web.route('/sync_from_anywhere', methods=['post'])
def handle_sync_from_anywhere():
    from api.anywhere.get_products import sync_products
    server_url = request.form['server_url']
    login_username = request.form['login_username']
    login_password = request.form['login_password']
    max_return = request.args.get('max')
    sync_products(server_url, login_username, login_password)

    data = urllib.parse.urlencode({'max_return': max_return}).encode('utf-8')
    url = config.ADMIN_SERVER_URL + 'partial_sync'
    req = urllib.request.Request(url=url, data=data)
    try:
        urllib.request.urlopen(req, timeout=3)
    except socket.timeout:
        return 'done'
    except Exception as e:
        return str(e)
    return 'done'


@app_web.route('/sync_from_b1', methods=['post'])
def handle_sync_from_b1():
    from api.b1.get_products import sync_products
    schema = request.form['schema']
    username = request.form['username']
    password = request.form['password']
    max_return = request.args.get('max')
    sync_products(schema, username, password)

    data = urllib.parse.urlencode({'max_return': max_return}).encode('utf-8')
    url = config.ADMIN_SERVER_URL + 'partial_sync'
    req = urllib.request.Request(url=url, data=data)
    try:
        urllib.request.urlopen(req, timeout=3)
    except socket.timeout:
        return 'done'
    except Exception as e:
        return str(e)
    return 'done'
