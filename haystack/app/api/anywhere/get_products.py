# -*- coding:utf-8 -*-

import os
import sys
sys.path.append('..' + os.path.sep + '..')

from conf import config
from db.db_operations import add_vendor_product
from utils.crawler import save_image
import requests
import json
import os


SERVER_URL = ''
LOGIN_USERNAME = ''
LOGIN_PASSWORD = ''
PROXIES = {}


def get_login_cookie(server, username, password):
    login_url = 'https://mp-' + server + '/login'
    params = {
        'username': username,
        'password': password
    }
    headers = {
        'content-type': 'application/json'
    }
    response = requests.request(
        'POST',
        login_url,
        headers=headers,
        json=params,
        verify=False,
        proxies=PROXIES
    )
    cookie = response.json()['cookie']
    return cookie


def get_products_info(server, username, password):
    cookie = get_login_cookie(server, username, password)
    api_url = 'https://go-' + SERVER_URL + '/api/mobile/Products/v1?expand=*'
    headers = {
        'content-type': 'application/json',
        'cookie': cookie
    }
    response = requests.request(
        'GET',
        api_url,
        headers=headers,
        verify=False,
        proxies=PROXIES
    )
    response = json.loads(response.text)
    products_info = []
    for r in response:
        if r.get('statusCode') != -1:
            products_info.append(r)
    return products_info


def get_skus_info(server, username, password):
    products = get_products_info(server, username, password)
    all_skus = []

    for product in products:
        skus = product['skus']
        price_list = product['productPrice']['priceList']
        attachment_list = product['attachmentList']

        # get currency code for standard price
        currency_code = None
        for l in price_list:
            if l['listType'] == 'standard':
                currency_code = l['currencyCode']
                break

        for tmp in skus:
            sku = {
                'id': tmp['id'],
                'name': tmp['name'],
                'standard_price': tmp['standardPrice'],
                'currency_code': currency_code
            }
            # get sku images, if not exist, use product images
            attachments = []
            for variant in tmp['variantList']:
                attachments.append(variant['attachmentList'])
            if len(attachments) == 0:
                attachments = attachment_list
            sku['images'] = attachments
            all_skus.append(sku)

    return all_skus


def sync_products(server, username, password):
    all_products = get_skus_info(server, username, password)
    for product in all_products:
        add_vendor_product(product.get('name'),
                           product.get('standard_price'),
                           product.get('currency_code'),
                           product.get('id'))
        for i, image in enumerate(product.get('images')):
            file_name = str(product.get('id')) + '_' + str(i)
            save_path = os.path.join(config.PRODUCT_IMAGE_DIR, file_name)
            save_image(image.get('url'), save_path)

        file_name = str(product.get('id'))
        save_path = os.path.join(config.PRODUCT_MAIN_IMAGE_DIR, file_name)
        save_image(product.get('images')[0].get('url'), save_path)
