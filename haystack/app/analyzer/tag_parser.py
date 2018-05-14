# -*- coding:utf-8 -*-

import os
import sys
sys.path.append('..' + os.path.sep)

from conf import config
from db.db_operations import check_site_by_id
from pyquery import PyQuery as pq
from utils.price_operation import price_formatter
import chardet
import datetime
import logging
import os
import re


LOGGER = logging.getLogger(__name__)


def get_price(site, rule):
    """
    get price according to tag selectors
    :param site: dict, {'site_id', 'product_site_id', 'url', 'product_name'}
    :param rule: rule of price_tag_selector.json
    :return: list of price information,
             [{'method': 'tag pattern', 'price', 'rule': {'selector', 'weight'}, 'event_time'}, ...]
    """
    error_flag = False
    price_list = []
    if not check_site_by_id(site.get('site_id')):
        return True, None
    raw_data_path = config.URL_CRAWLED_DATA_DIR
    data_file_path = raw_data_path + str(site.get('site_id'))
    new_data_file_path = raw_data_path + str(site.get('site_id')) + '_new'
    if not os.path.exists(new_data_file_path) and not os.path.exists(data_file_path):
        LOGGER.warning('tag pattern: cannot crawl data from this url')
        return True, None

    if os.path.exists(new_data_file_path):
        error_flag, price_list, selector_list = parse_price(new_data_file_path, rule.get('containers'), rule.get('selectors'))
    else:
        selector_list = rule.get('selectors')

    if selector_list and len(selector_list) > 0:
        if os.path.exists(data_file_path):
            error_flag, price_list2, selector_list2 = parse_price(data_file_path, rule.get('containers'), selector_list)
            if price_list2:
                price_list += price_list2

    if price_list and len(price_list) > 0:
        LOGGER.info('[SUCCESS] tag pattern: ' + str(price_list))
        return error_flag, price_list
    else:
        LOGGER.info('[FAIL] tag pattern: no tag matched')
        return error_flag, None


def parse_price(file, containers, selectors):
    """
    parse price
    :param file: raw data file path
    :param containers: containers in price_tag_selectors.json
    :param selectors: selectors in price_tag_selectors.json
    :return: True if error, else False
    :return: list of price information,
             [{'method': 'tag pattern', 'price', 'currency', 'rule': {'selector', 'weight'}, 'event_time'}, ...]
    :return: selectors failed to parse price
    """
    with open(file, 'rb') as f:
        content = f.read()
    encoding = chardet.detect(content)['encoding']
    try:
        content = content.decode(encoding)
    except UnicodeDecodeError as e:
        try:
            content = content.decode('utf-8')
        except Exception as e:
            print('[FAIL] tag pattern:', e)
            LOGGER.warning('tag pattern: ' + str(e))
            return True, None, None
    except Exception as e:
        print('[FAIL] tag pattern:', e)
        LOGGER.warning('tag pattern: ' + str(e))
        return True, None, None

    try:
        doc = pq(content)
    except Exception as e:
        LOGGER.warning('tag pattern: ' + str(e))
        return True, None, None
    price_list = []
    selector_list = []
    for tag in selectors:
        prices = doc(tag.get('selector'))
        success_flag = False
        if prices:
            if prices.size() == 1:
                container = re.match(r'(<)(\w+)(\s*|/>)(\.*)', str(prices)).group(2)
                if container and container in containers:
                    price, currency = price_formatter(prices.text())
                    if price and price != '' and float(price) != 0:
                        price_list.append({
                            'method': 'tag pattern',
                            'price': price,
                            'currency': currency,
                            'rule': {
                                'selector': tag.get('selector'),
                                'weight': tag.get('weight'),
                            },
                            'event_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        })
                        success_flag = True
            elif prices.size() > 1:
                i = 0
                while i < prices.size():
                    price = prices.eq(i)
                    container = re.match(r'(<)(\w+)(\s*|/>)(\.*)', str(price)).group(2)
                    if container and container in containers:
                        price, currency = price_formatter(price.text())
                        if price and price != '' and float(price) != 0:
                            price_list.append({
                                'method': 'tag pattern',
                                'price': price,
                                'currency': currency,
                                'rule': {
                                    'selector': tag.get('selector'),
                                    'weight': tag.get('weight'),
                                },
                                'event_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            })
                            success_flag = True
                            break
                    i += 1
        if not success_flag:
            selector_list.append(tag)
    return False, price_list, selector_list
