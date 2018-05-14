# -*- coding:utf-8 -*-

import os
import sys
sys.path.append('..' + os.path.sep)

from analyzer import MagicHayStack
from analyzer import tag_parser
from analyzer import url_profile_parser
from analyzer.microdata_filter import microdata_filter
from conf import config
from db.db_operations import add_event, set_site_finished, get_site_domain
from utils.crawler import crawl_data
from utils.snip_website import snip_website
import datetime
import json
import os


def get_price(site_id, site_data, need_screenshot=True):
    page_url = site_data.get('url')
    image_urls = site_data.get('image_urls')
    print(page_url)

    need_retry = False
    try:
        if not crawl_data(page_url, site_id, max_retry_times=1):
            need_retry = True
            return need_retry

        # filter by microdata
        print('=> microdata filter')
        success_flag, price, currency, event_time = microdata_filter(site_id)
        if success_flag:
            add_event(site_id, price, currency, event_time)
            # set_site_finished(site_id)
            print('[SUCCESS]', currency, price, event_time)

            # snipping website
            if need_screenshot:
                screenshot_name = os.path.join(config.SITE_SCREENSHOT_DIR, str(site_id) + '.png')
                if not os.path.exists(screenshot_name):
                    try:
                        snip_website(page_url, screenshot_name)
                    except Exception as e:
                        print(e)
            return need_retry

        # url pattern analyzer
        print('=> url pattern analyzer')
        url_profiles_path = os.path.join(config.RULE_DIR, 'url_profiles.json')
        url_pattern_result = url_pattern_analyzer(url_profiles_path, site_id)
        if url_pattern_result:
            add_event(site_id,
                      url_pattern_result.get('price'),
                      url_pattern_result.get('currency'),
                      url_pattern_result.get('event_time'))
            # set_site_finished(site_id)
            print('[SUCCESS]',
                  url_pattern_result.get('currency'),
                  url_pattern_result.get('price'),
                  url_pattern_result.get('event_time'))

            # snipping website
            if need_screenshot:
                screenshot_name = os.path.join(config.SITE_SCREENSHOT_DIR, str(site_id) + '.png')
                if not os.path.exists(screenshot_name):
                    try:
                        snip_website(page_url, screenshot_name)
                    except Exception as e:
                        print(e)
            return need_retry

        print('=> tag pattern analyzer')
        results = []
        # tag analyzer
        price_tag_selectors_path = os.path.join(config.RULE_DIR, 'price_tag_selectors.json')
        error_flag, tag_pattern_results = tag_pattern_analyzer(price_tag_selectors_path, site_id)
        # magic analyzer
        print('=> magic analyzer')
        magic_result = magic_analyzer({'site_id': site_id, 'url': page_url}, image_urls)

        if tag_pattern_results or magic_result:
            if tag_pattern_results and magic_result:
                results.extend(tag_pattern_results)
                for mr in magic_result:
                    for r in results:
                        if r.get('price') == mr.get('price'):
                            r['rule']['weight'] += mr.get('rule').get('weight')
                            r['currency'] = r['currency'] if r['currency'] else mr['currency']
                            r['method'] += ' + magic'
                            r['rule']['selector'] += ' + magic'
            else:
                results.extend(tag_pattern_results if tag_pattern_results else magic_result)

            results.sort(key=lambda x: float(x.get('rule').get('weight')), reverse=True)
            best_result = results[0]
            add_event(site_id, best_result.get('price'), best_result.get('currency'), best_result.get('event_time'))
            # set_site_finished(site_id)
            print('[SUCCESS]', best_result.get('price'), best_result.get('currency'), best_result.get('event_time'))

            # snipping website
            if need_screenshot:
                screenshot_name = os.path.join(config.SITE_SCREENSHOT_DIR, str(site_id) + '.png')
                if not os.path.exists(screenshot_name):
                    try:
                        snip_website(page_url, screenshot_name)
                    except Exception as e:
                        print(e)
            return need_retry

    except Exception as e:
        print(str(e))
        return need_retry


def url_pattern_analyzer(url_profiles_path, site_id):
    with open(url_profiles_path) as f:
        url_profiles = json.load(f)
    domain = get_site_domain(site_id)
    if not domain:
        return None
    rule = url_profiles.get(domain)
    if not rule:
        return None

    success_flag = False
    try:
        success_flag, price, currency, event_time = url_profile_parser.get_price(site_id, rule)
    except Exception as e:
        print(e)

    if success_flag:
        p = {
            'method': 'url pattern',
            'price': price,
            'currency': currency,
            'event_time': event_time,
            'rule': {'selector': domain, 'weight': 2.0}
        }
    else:
        print('[FAIL] url pattern: price not found')
    return p if success_flag else None


def tag_pattern_analyzer(selector_path, site_id):
    """
    analyse url according to some tag rules
    :param selector_path: selector json file path
    :param site: dict, {'site_id', 'product_site_id', 'url', 'product_name'}
    :return: [{'method': 'tag pattern', 'price', 'rule': {'selector', 'weight'}, 'event_time'}, ...]
    """
    with open(selector_path) as f:
        tag_selectors = json.load(f)

    error_flag = True
    ret = None
    try:
        error_flag, ret = tag_parser.get_price(site_id, tag_selectors)
    except Exception as e:
        print(e)
    return error_flag, ret


def magic_analyzer(site, image_urls):
    """
    analyse url in some magic ways, such as ML
    :param site: dict, {'site_id', 'product_site_id', 'url', 'product_name'}
    :param image_urls: list
    :return: [{'method': 'url pattern', 'price', 'currency', 'rule': {'selector', 'weight'}, 'event_time'}]
    """
    res = None
    try:
        res = MagicHayStack.get_price(site.get('url'), image_urls)
    except Exception as e:
        print(str(e))

    if not res:
        print('[FAIL] magic: price not found')
        return None
    else:
        p = []
        for r in res:
            if r[0]:
                p.append({
                    'method': 'magic',
                    'price': r[0],
                    'currency': r[1],
                    'rule': {
                        'selector': 'magic',
                        'weight': r[2]
                    },
                    'event_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
        if not p:
            print('[FAIL] magic: price not found')
            return None
        else:
            print('[SUCCESS] magic:', p)
            return p
