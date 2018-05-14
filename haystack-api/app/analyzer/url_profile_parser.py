# -*- coding:utf-8 -*-

import os
import sys
sys.path.append('..' + os.path.sep)

from conf import config
from pyquery import PyQuery as pq
from utils.price_operation import price_formatter
import chardet
import datetime
import logging
import os
import re


LOGGER = logging.getLogger(__name__)


def get_price(site_id, rule):
    raw_data_path = config.URL_CRAWLED_DATA_DIR
    data_file_path = raw_data_path + str(site_id)
    if not os.path.exists(data_file_path):
        return False, None, None, None

    # parse url
    ret = None
    price = None

    is_list_empty = True if len(rule['list']) == 0 else False
    if not is_list_empty:
        for l in rule['list']:
            ret = parse_list(data_file_path, l)

    if ret:
        price = ret[0].get('price')
    if not ret or is_list_empty:
        price = parse_single_price(data_file_path, rule['item']['price'])

    if not price:
        return False, None, None, None
    else:
        return (
            True, price, rule['currency'],
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )


def parse_single_price(path, rule):
    """
    for item page, to parse price information
    :param path: path of the raw data file
    :param rule: rule for parsing
    :return: price
    """
    with open(path, 'rb') as f:
        content = f.read()
    encoding = chardet.detect(content)['encoding']
    try:
        content = content.decode(encoding)
    except UnicodeDecodeError:
        try:
            content = content.decode('utf-8')
        except Exception as e:
            print(str(e))
            return None
    except Exception as e:
        print(str(e))
        return None

    doc = pq(content)
    price = doc(rule['selector']).filter(lambda x, this: re.compile(rule['filter_re']).match(
        pq(this).attr(rule['filter_attr']) if rule['filter_in_attr'] else pq(this).html()
    )) if rule['filter'] else doc(rule['selector'])
    price = price.children() if rule['children'] else price
    if not price:
        return None
    price = pq(price).attr(rule['attr']) if rule['in_attr'] else pq(price).text()
    price, currency = price_formatter(price)
    return price


def parse_list(path, rule):
    """
    for list page, to parse name and price information
    :param path: path of the raw data file
    :param rule: rule for parsing
    :return: ret, list of information
    """
    with open(path, 'rb') as f:
        content = f.read()
    encoding = chardet.detect(content)['encoding']
    try:
        content = content.decode(encoding)
    except UnicodeDecodeError:
        try:
            content = content.decode('utf-8')
        except Exception as e:
            print(str(e))
            return None
    except Exception as e:
        print(str(e))
        return None

    doc = pq(content)

    list_exist = doc(rule['selector'])
    if not list_exist:
        return None

    ret = []
    items = doc(rule['item_selector'])
    for i in range(0, items.size()):
        item = items.eq(i)
        description = None
        price = None
        # Parse description
        for it in item.items(rule['item_description']['selector']):
            description = it.eq(0)
        if description:
            description = description.filter(
                lambda x, this: re.compile(rule['item_description']['filter_re']).match(
                    pq(this).attr(rule['item_description']['filter_attr'])
                    if rule['item_price']['filter_in_attr'] else pq(this).html())
            ) if rule['item_description']['filter'] else description
            description = description.children() if rule['item_description']['children'] else description
            if description:
                description = pq(description).attr(rule['item_description']['attr']) \
                    if rule['item_description']['in_attr'] else description.text()
        # Parse price
        for it in item.items(rule['item_price']['selector']):
            price = it.eq(0)
        if price:
            price = price.filter(
                lambda x, this: re.compile(rule['item_price']['filter_re']).match(
                    pq(this).attr(rule['item_price']['filter_attr'])
                    if rule['item_price']['filter_in_attr'] else pq(this).html())
            ) if rule['item_price']['filter'] else price
            price = price.children() if rule['item_price']['children'] else price
            if price:
                price = pq(price).attr(rule['item_price']['attr']) \
                    if rule['item_price']['in_attr'] else pq(price).text()
                price, currency = price_formatter(price)
        ret.append({'name': description, 'price': price})

    return ret
