# -*- coding:utf-8 -*-

import os
import sys
sys.path.append('..' + os.path.sep + '..')

from conf import config
from db.db_operations import add_vendor_product
from utils.price_operation import currency_formatter
import requests
import json
import os


SCHEMA = ''
USERNAME = ''
PASSWORD = ''

LOGIN_REQ_URL = ''
LOGIN_REQ_DOMAIN = ''
PRODUCT_REQ_URL = ''
DETAIL_REQ_URL = ''
IMAGE_REQ_URL = ''

COOKIE_KEY = ''


def get_login_cookie(schema, username, password):
    request_url = LOGIN_REQ_URL
    request_headers = {
        'Content-Type': 'application/json'
    }
    request_data = {
        'schema': schema,
        'username': username,
        'password': password
    }
    response = requests.request(
        'POST',
        request_url,
        headers=request_headers,
        data=json.dumps(request_data)
    )
    cookie = response.cookies[COOKIE_KEY]
    return cookie


def get_products(schema, username, password):
    request_url = PRODUCT_REQ_URL
    request_headers = {
        'Content-Type': 'application/json'
    }
    jar = requests.cookies.RequestsCookieJar()
    jar.set(
        'JSESSIONID',
        get_login_cookie(schema, username, password),
        domain=LOGIN_REQ_DOMAIN,
        path='/app-web'
    )
    requests.request(
        'GET',
        request_url,
        headers=request_headers,
        cookies=jar
    )
    request_url = PRODUCT_REQ_URL
    response = requests.request(
        'GET',
        request_url,
        headers=request_headers,
        cookies=jar
    )
    response = json.loads(response.text)

    products = []
    for r in response.get('d').get('results'):
        product_id = r.get('id')
        detail_request_url = DETAIL_REQ_URL + product_id
        detail_response = requests.request(
            'GET',
            detail_request_url,
            headers=request_headers,
            cookies=jar
        )
        detail_response = json.loads(detail_response.text)
        detail_response_price = detail_response.get('data')[0].get('VPrice').get('value')
        if not detail_response_price:
            continue
        products.append({
            'id': product_id,
            'product_name': r.get('ItemName').get('value'),
            'price': detail_response_price.get('amount'),
            'currency': currency_formatter(detail_response_price.get('unit')),
            'image_name': r.get('PicturName').get('value')
        })
    print(products)
    return products


def save_image(image_name, save_path, schema, username, password):
    request_url = IMAGE_REQ_URL + image_name
    jar = requests.cookies.RequestsCookieJar()
    jar.set(
        COOKIE_KEY,
        get_login_cookie(schema, username, password),
        domain=LOGIN_REQ_DOMAIN,
        path='/app-web'
    )
    response = requests.request('GET', request_url, cookies=jar)
    with open(save_path, 'wb') as f:
        f.write(response)


def sync_product(schema, username, password):
    products = get_products(schema, username, password)
    for product in products:
        add_vendor_product(product.get('product_name'),
                           product.get('price'),
                           product.get('currency'),
                           product.get('id'))
        file_name = str(product.get('image_name'))
        save_path = os.path.join(config.PRODUCT_MAIN_IMAGE_DIR, file_name)
        save_image(product.get('image_name'), save_path, schema, username, password)

