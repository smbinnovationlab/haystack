# -*- coding:utf-8 -*-

import os
import sys
sys.path.append('..' + os.path.sep)

from analyzer import url_profile_parser
from conf import config
from db.db_operations import add_event, set_site_finished, get_site_domain
from utils.snip_website import snip_website
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

    url_pattern_time_cost = 0.0
    screenshot_time_cost = 0.0

    try:
        start_time = timeit.default_timer()

        # url pattern analyzer
        url_profiles_path = os.path.join(config.RULE_DIR, 'url_profiles.json')
        url_pattern_result = url_pattern_analyzer(url_profiles_path, site_id)
        url_pattern_time_cost = timeit.default_timer() - start_time
        if url_pattern_result:
            add_event(site_id,
                      url_pattern_result.get('price'),
                      url_pattern_result.get('currency'),
                      url_pattern_result.get('event_time'))

            LOGGER.info('[#] (%s) (2nd) %s' % (str(retry_times), page_url,))
            LOGGER.info('[V] (%s) (2nd) Price found: <url pattern> (%s %s)' % (str(retry_times),
                                                                               str(url_pattern_result.get('currency')),
                                                                               str(url_pattern_result.get('price')),))
            LOGGER.info('[T] (%s) (2nd) %ss' % (str(retry_times), str(url_pattern_time_cost),))

            # snipping website
            if need_screenshot:
                screenshot_name = os.path.join(config.SITE_SCREENSHOT_DIR, str(site_id) + '.png')
                if not os.path.exists(screenshot_name):
                    try:
                        start_time = timeit.default_timer()
                        snip_website(page_url, screenshot_name)
                        screenshot_time_cost = timeit.default_timer() - start_time
                        LOGGER.info('[#] (%s) (2nd) %s' % (str(retry_times), page_url,))
                        LOGGER.info('[V] (%s) (2nd) Get screenshot successfully' % (str(retry_times),))
                        LOGGER.info('[T] (%s) (2nd) %ss' % (str(retry_times), str(screenshot_time_cost),))
                    except Exception as e:
                        LOGGER.warning('[#] (%s) (2nd) %s' % (str(retry_times), page_url,))
                        LOGGER.warning('[X] (%s) (2nd) Fail to get screenshot: %s' % (str(retry_times), str(e),))
            return 1, url_pattern_time_cost, screenshot_time_cost
        else:
            LOGGER.info('[#] (%s) (2nd) %s' % (str(retry_times), page_url,))
            LOGGER.info('[X] (%s) (2nd) Price not found: <url pattern>' % (str(retry_times),))
            LOGGER.info('[T] (%s) (2nd) %ss' % (str(retry_times), str(url_pattern_time_cost),))
            return 0, url_pattern_time_cost, screenshot_time_cost
    except Exception as e:
        LOGGER.warning('[#] (%s) (2nd) %s' % (str(retry_times), page_url,))
        LOGGER.warning('[X] (%s) (2nd) Exception in get_price: %s' % (str(retry_times), str(e),))
        return -1, 0.0, 0.0


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
