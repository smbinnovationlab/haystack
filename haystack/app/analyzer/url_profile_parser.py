# -*- coding:utf-8 -*-

import os
import sys
sys.path.append('..' + os.path.sep)

from conf import config
from db.db_operations import check_site_by_id, update_events, update_site
from pyquery import PyQuery as pq
from utils.find_best_match import find_best_match
from utils.price_operation import price_formatter
import chardet
import datetime
import logging
import os
import re


LOGGER = logging.getLogger(__name__)


def get_price(site, rule):
    """
    main function to parse an url
    :param site: dict, {'site_id', 'product_site_id', 'url', 'product_name'}
    :param rule: rule in url_profiles.json
    """
    if not check_site_by_id(site.get('site_id')):
        return False, None, None, None
    raw_data_path = config.URL_CRAWLED_DATA_DIR
    data_file_path = raw_data_path + str(site.get('site_id'))
    new_data_file_path = raw_data_path + str(site.get('site_id')) + '_new'
    if not os.path.exists(new_data_file_path) and not os.path.exists(data_file_path):
        LOGGER.warning('url pattern: cannot crawl data from this url')
        return False, None, None, None

    # parse url
    ret = None
    price = None
    site_type = None

    is_list_empty = (True if len(rule['list']) == 0 else False)
    if not is_list_empty:
        if os.path.exists(new_data_file_path):
            for l in rule['list']:
                ret = parse_list(new_data_file_path, l)
                if ret:
                    site_type = l['type']
                    if os.path.exists(data_file_path):
                        os.remove(data_file_path)
                    os.rename(new_data_file_path, data_file_path)
                    break
            if not ret and os.path.exists(data_file_path):
                os.remove(new_data_file_path)
                for l in rule['list']:
                    ret = parse_list(data_file_path, l)
                    if ret:
                        break
        if ret:
            temp = find_best_match(ret, site.get('product_name'))
            price = temp.get('price')
    if not ret or is_list_empty:
        site_type = rule['item']['type']
        if os.path.exists(new_data_file_path):
            price = parse_single_price(new_data_file_path, rule['item']['price'])
            if not price:
                if os.path.exists(data_file_path):
                    os.remove(new_data_file_path)
                    price = parse_single_price(data_file_path, rule['item']['price'])
            else:
                if os.path.exists(data_file_path):
                    os.remove(data_file_path)
                os.rename(new_data_file_path, data_file_path)
        elif os.path.exists(data_file_path):
            price = parse_single_price(data_file_path, rule['item']['price'])

    if not price:
        return False, None, None, None
    else:

        site_country = rule['country']
        update_site(site.get('site_id'), site_type, site_country)
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
            LOGGER.warning('url pattern: ' + str(e))
            return None
    except Exception as e:
        LOGGER.warning('url pattern: ' + str(e))
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
            # print('[FAIL] url pattern:', e)
            LOGGER.warning('url pattern: ' + str(e))
            return None
    except Exception as e:
        # print('[FAIL] url pattern:', e)
        LOGGER.warning('url pattern: ' + str(e))
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
