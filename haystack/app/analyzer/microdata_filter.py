# -*- coding:utf-8 -*-

import os
import sys
sys.path.append('..' + os.path.sep)

from conf import config
from db.db_operations import check_site_by_id, update_events
from utils.find_best_match import find_best_match
from utils.price_operation import price_formatter
import chardet
import datetime
import json
import logging
import microdata
import os


LOGGER = logging.getLogger(__name__)


def microdata_filter(site):
    """
    filter site contains microdata
    follows the schema in 'http://schema.org/Product'
    :param site: dict, {'site_id', 'product_site_id', 'url', 'product_name'}
    :return: success_flag, currency, price
    """
    success_flag = False
    if not check_site_by_id(site.get('site_id')):
        return success_flag, None, None, None

    products = []
    schema_product_type = 'http://schema.org/Product'

    data_file_path = config.URL_CRAWLED_DATA_DIR + str(site.get('site_id'))
    new_data_file_path = config.URL_CRAWLED_DATA_DIR + str(site.get('site_id')) + '_new'
    if not os.path.exists(new_data_file_path) and not os.path.exists(data_file_path):
        LOGGER.warning('microdata: cannot crawl data from this url')
        return False, None, None, None

    items = None
    if os.path.exists(new_data_file_path):
        with open(new_data_file_path, 'rb') as f:
            encoding = chardet.detect(f.read())['encoding']
            items = microdata.get_items(f, encoding)
    if not items:
        if os.path.exists(new_data_file_path) and os.path.exists(data_file_path):
            os.remove(new_data_file_path)
        if os.path.exists(data_file_path):
            with open(data_file_path, 'rb') as f:
                encoding = chardet.detect(f.read())['encoding']
                items = microdata.get_items(f, encoding)
    else:
        if os.path.exists(data_file_path):
            os.remove(data_file_path)
        os.rename(new_data_file_path, data_file_path)

    for item in items:
        item = json.loads(item.json())
        if item.get('type')[0] == schema_product_type and item.get('properties').get('offers'):
            success_flag = True
            product_name = None
            product_price = None
            product_currency = None
            try:
                product_name = item.get('properties').get('name')[0]
            except Exception as e:
                LOGGER.warning('microdata: ' + str(e))
            try:
                product_price = item.get('properties').get('offers')[0].get('properties').get('price')[0]
            except Exception as e:
                LOGGER.warning('microdata: ' + str(e))
            try:
                product_currency = item.get('properties').get('offers')[0].get('properties').get('priceCurrency')[0]
            except Exception as e:
                LOGGER.warning('microdata: ' + str(e))

            if product_price:
                product = {
                    'name': product_name,
                    'price': price_formatter(product_price)[0] if product_price else None,
                    'currency': product_currency
                }
                products.append(product)

    if len(products) == 0:
        LOGGER.info('[FAIL] microdata: not found')
        return success_flag, None, None, None
    elif len(products) == 1:
        product = products[0]
    else:
        product = find_best_match(products, site.get('product_name'))

    LOGGER.info('[RESULT] microdata: ' + str(product.get('currency')) + ' ' + str(product.get('price')))
    return success_flag, product.get('price'), product.get('currency'), \
           datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
