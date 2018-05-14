# -*- coding:utf-8 -*-

import os
import sys
sys.path.append('..' + os.path.sep)

from analyzer import MagicHayStack
from analyzer import tag_parser
from conf import config
from db.db_operations import add_event, set_site_finished, get_site_domain
from utils.snip_website import snip_website
import datetime
import json
import logging
import os
import timeit


LOGGER = logging.getLogger(__name__)


def get_price(site_id, site_data, need_screenshot=True):
    """
    :param site_id:
    :param site_data:
    :param need_screenshot:
    :return: [INT] -1 for retry, 0 for fail, 1 for success
    """
    page_url = site_data.get('url')
    image_urls = site_data.get('image_urls')
    retry_times = site_data.get('retry_times')

    tag_pattern_time_cost = 0.0
    ml_time_cost = 0.0
    screenshot_time_cost = 0.0

    try:
        start_time = timeit.default_timer()

        results = []
        # tag analyzer
        price_tag_selectors_path = os.path.join(config.RULE_DIR, 'price_tag_selectors.json')
        error_flag, tag_pattern_results = tag_pattern_analyzer(price_tag_selectors_path, site_id)
        tag_pattern_time_cost = timeit.default_timer() - start_time
        # magic analyzer
        magic_result = magic_analyzer({'site_id': site_id, 'url': page_url}, image_urls)
        ml_time_cost = timeit.default_timer() - start_time

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

            LOGGER.info('[#] (%s) (2nd) %s' % (str(retry_times), page_url,))
            LOGGER.info('[V] (%s) (2nd) Price found: <url pattern> (%s %s)' % (str(retry_times),
                                                                               str(best_result.get('currency')),
                                                                               str(best_result.get('price')),))
            LOGGER.info('[T] (%s) (2nd) %ss' % (str(retry_times), str(tag_pattern_time_cost + ml_time_cost),))

            # snipping website
            if need_screenshot:
                screenshot_name = os.path.join(config.SITE_SCREENSHOT_DIR, str(site_id) + '.png')
                if not os.path.exists(screenshot_name):
                    try:
                        start_time = timeit.default_timer()
                        snip_website(page_url, screenshot_name)
                        screenshot_time_cost = timeit.default_timer() - start_time
                        LOGGER.info('[#] (%s) (3rd) %s' % (str(retry_times), page_url,))
                        LOGGER.info('[V] (%s) (3rd) Get screenshot successfully' % (str(retry_times),))
                        LOGGER.info('[T] (%s) (3rd) %ss' % (str(retry_times), str(screenshot_time_cost),))
                    except Exception as e:
                        LOGGER.warning('[#] (%s) (3rd) %s' % (str(retry_times), page_url,))
                        LOGGER.warning('[X] (%s) (3rd) Fail to get screenshot: %s' % (str(retry_times), str(e),))
            return 1, tag_pattern_time_cost, ml_time_cost, screenshot_time_cost
        else:
            LOGGER.info('[#] (%s) (3rd) %s' % (str(retry_times), page_url,))
            LOGGER.info('[X] (%s) (3rd) Price not found: <tag pattern + ML>' % (str(retry_times),))
            LOGGER.info('[T] (%s) (2nd) %ss' % (str(retry_times), str(tag_pattern_time_cost + ml_time_cost),))
            return 0, tag_pattern_time_cost, ml_time_cost, screenshot_time_cost
    except Exception as e:
        LOGGER.warning('[#] (%s) (3rd) %s' % (str(retry_times), page_url,))
        LOGGER.warning('[X] (%s) (3rd) Exception in get_price: %s' % (str(retry_times), str(e),))
        return -1, 0.0, 0.0, 0.0


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
