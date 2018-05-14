# -*- coding:utf-8 -*-

import os
import sys
sys.path.append('..' + os.path.sep)

from conf import config
from utils.price_operation import price_formatter
import chardet
import datetime
import json
import logging
import microdata
import os


LOGGER = logging.getLogger(__name__)


def microdata_filter(site_id):
    products = []
    schema_product_type = 'http://schema.org/Product'

    data_file_path = config.URL_CRAWLED_DATA_DIR + str(site_id)
    if not os.path.exists(data_file_path):
        return False, None, None, None

    with open(data_file_path, 'rb') as f:
        encoding = chardet.detect(f.read())['encoding']
        items = microdata.get_items(f, encoding)
    if not items:
        return False, None, None, None

    for item in items:
        item = json.loads(item.json())
        if item.get('type')[0] == schema_product_type and item.get('properties').get('offers'):
            product_price = None
            product_currency = None
            try:
                product_price = item.get('properties').get('offers')[0].get('properties').get('price')[0]
            except Exception as e:
                print(e)
            try:
                product_currency = item.get('properties').get('offers')[0].get('properties').get('priceCurrency')[0]
            except Exception as e:
                print(e)

            if product_price:
                product = {
                    'price': price_formatter(product_price)[0] if product_price else None,
                    'currency': product_currency
                }
                products.append(product)

    if len(products) == 0:
        return False, None, None, None
    else:
        product = products[0]
        return True, product.get('price'), product.get('currency'), datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
