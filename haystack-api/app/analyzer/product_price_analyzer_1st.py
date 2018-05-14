# -*- coding:utf-8 -*-

import os
import sys
sys.path.append('..' + os.path.sep)

from analyzer.microdata_filter import microdata_filter
from conf import config
from db.db_operations import add_event, set_site_finished, get_site_domain
from utils.crawler import crawl_data
from utils.snip_website import snip_website
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

    crawl_time_cost = 0.0
    microdata_time_cost = 0.0
    screenshot_time_cost = 0.0

    try:
        start_time = timeit.default_timer()

        success_to_crawl = crawl_data(page_url, site_id, max_retry_times=1)
        if not success_to_crawl:
            LOGGER.warning('[#] (%s) (1st) %s' % (str(retry_times), page_url,))
            LOGGER.warning('[X] (%s) (1st) Failed to crawl. Retry' % (str(retry_times),))
            return -1, 0.0, 0.0, 0.0
        else:
            crawl_time_cost = timeit.default_timer() - start_time
            LOGGER.info('[#] (%s) (1st) %s' % (str(retry_times), page_url,))
            LOGGER.info('[V] (%s) (1st) Crawled successfully' % (str(retry_times),))
            LOGGER.info('[T] (%s) (1st) %ss' % (str(retry_times), str(crawl_time_cost),))

        start_time = timeit.default_timer()
        # filter by microdata
        success_flag, price, currency, event_time = microdata_filter(site_id)
        microdata_time_cost = timeit.default_timer() - start_time
        if success_flag:
            add_event(site_id, price, currency, event_time)

            LOGGER.info('[#] (%s) (1st) %s' % (str(retry_times), page_url,))
            LOGGER.info('[V] (%s) (1st) Price found: <microdata> (%s %s)' % (str(retry_times),
                                                                             str(currency),
                                                                             str(price),))
            LOGGER.info('[T] (%s) (1st) %ss' % (str(retry_times), str(microdata_time_cost),))

            # snipping website
            if need_screenshot:
                screenshot_name = os.path.join(config.SITE_SCREENSHOT_DIR, str(site_id) + '.png')
                if not os.path.exists(screenshot_name):
                    try:
                        start_time = timeit.default_timer()
                        snip_website(page_url, screenshot_name)
                        screenshot_time_cost = timeit.default_timer() - start_time
                        LOGGER.info('[#] (%s) (1st) %s' % (str(retry_times), page_url,))
                        LOGGER.info('[V] (%s) (1st) Get screenshot successfully' % (str(retry_times),))
                        LOGGER.info('[T] (%s) (1st) %ss' % (str(retry_times), str(screenshot_time_cost),))
                    except Exception as e:
                        LOGGER.warning('[#] (%s) (1st) %s' % (str(retry_times), page_url,))
                        LOGGER.warning('[X] (%s) (1st) Fail to get screenshot: %s' % (str(retry_times), str(e),))
            return 1, crawl_time_cost, microdata_time_cost, screenshot_time_cost
        else:
            LOGGER.info('[#] (%s) (1st) %s' % (str(retry_times), page_url,))
            LOGGER.info('[X] (%s) (1st) Price not found: <microdata>' % (str(retry_times),))
            LOGGER.info('[T] (%s) (1st) %ss' % (str(retry_times), str(microdata_time_cost),))
            return 0, crawl_time_cost, microdata_time_cost, screenshot_time_cost
    except Exception as e:
        LOGGER.warning('[#] (%s) (1st) %s' % (str(retry_times), page_url,))
        LOGGER.warning('[X] (%s) (1st) Exception in get_price: %s' % (str(retry_times), str(e),))
        return -1, 0.0, 0.0, 0.0
