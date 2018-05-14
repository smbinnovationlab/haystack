# -*- coding:utf-8 -*-

import os
import sys
sys.path.append('..' + os.path.sep)

from analyzer import MagicHayStack
from analyzer import tag_parser
from analyzer import url_profile_parser
from analyzer.microdata_filter import microdata_filter
from conf import config
from db.db_operations import check_site_by_id, get_sites, get_site_domain, update_events, get_image_urls
from db.db_operations import update_site_status
from utils.crawler import crawl_data
from utils.snip_website import snip_website
import datetime
import json
import logging
import os
import time
import _locale


_locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])
LOGGER = logging.getLogger(__name__)


def get_price(product_id, need_screenshot=True):
    """
    main analyse operation
    :param product_id: product id
    :return: [{'url', 'status', 'rule', 'price', 'currency', 'all': {'rule', 'price', 'currency'}}, ...]
    """
    ret = []
    result_cnt = {
        'all': 0,
        'microdata': 0,
        'crawl error': 0,
        'not found': 0,
        'url pattern': 0,
        'tag pattern': 0,
        'magic': 0,
        'tag pattern + magic': 0
    }

    # get all sites
    sites = get_sites(product_id)
    image_urls = get_image_urls(product_id)
    all_data = {'sites': sites, 'image_urls': image_urls}
    result_cnt['all'] += len(sites)
    LOGGER.info('# %s => %s found' % (product_id, len(sites)))

    for site in all_data.get('sites'):
        print(site.get('url'))
        try:
            LOGGER.info('[URL] ' + str(site.get('url')))
        except Exception as e:
            LOGGER.error(str(e))
        # crawl raw data
        try:
            if not crawl_data(site.get('url'), site.get('site_id'), max_retry_times=3):
                result_cnt['crawl error'] += 1
                ret.append({'url': site.get('url'), 'status': 'crawl error'})
                LOGGER.warning('failed to crawl data')
                update_site_status(site.get('product_site_id'))
                continue
            else:
                LOGGER.info('[SUCCESS] crawl data')

            # filter by microdata
            success_flag, price, currency, event_time = microdata_filter(site)
            if success_flag:
                result_cnt['microdata'] += 1
                event = {
                    'product_site_id': site.get('product_site_id'),
                    'event_time': event_time,
                    'product_price': price,
                    'currency': currency
                }
                update_events(event)
                ret.append({
                    'url': site.get('url'),
                    'status': 'microdata',
                    'price': price,
                    'currency': currency
                })
                update_site_status(site.get('product_site_id'))
                # snipping website
                if need_screenshot:
                    screenshot_name = os.path.join(config.SITE_SCREENSHOT_DIR, str(site.get('product_site_id')) + '.png')
                    if not os.path.exists(screenshot_name):
                        try:
                            snip_website(site.get('url'), screenshot_name)
                            LOGGER.info('[SUCCESS] snipping website')
                        except Exception as e:
                            LOGGER.warning('snipping: ' + str(e))
                continue

            # url pattern analyzer
            url_profiles_path = os.path.join(config.RULE_DIR, 'url_profiles.json')
            url_pattern_result = url_pattern_analyzer(url_profiles_path, site)
            if url_pattern_result:
                result_cnt[url_pattern_result.get('method')] += 1
                event = {
                    'product_site_id': site.get('product_site_id'),
                    'event_time': url_pattern_result.get('event_time'),
                    'product_price': url_pattern_result.get('price'),
                    'currency': url_pattern_result.get('currency')
                }
                update_events(event)
                ret.append({
                    'url': site.get('url'),
                    'status': url_pattern_result.get('method'),
                    'price': url_pattern_result.get('price'),
                    'currency': url_pattern_result.get('currency'),
                    'rule': url_pattern_result.get('rule')
                })
                update_site_status(site.get('product_site_id'))
                # snipping website
                if need_screenshot:
                    screenshot_name = os.path.join(config.SITE_SCREENSHOT_DIR, str(site.get('product_site_id')) + '.png')
                    if not os.path.exists(screenshot_name):
                        try:
                            snip_website(site.get('url'), screenshot_name)
                            LOGGER.info('[SUCCESS] snipping website')
                        except Exception as e:
                            LOGGER.warning('snipping: ' + str(e))
                continue

            results = []
            # tag analyzer
            price_tag_selectors_path = os.path.join(config.RULE_DIR, 'price_tag_selectors.json')
            error_flag, tag_pattern_results = tag_pattern_analyzer(price_tag_selectors_path, site)
            # magic analyzer
            magic_result = magic_analyzer(site, all_data.get('image_urls'))
            if not tag_pattern_results and not magic_result:
                # price not found
                result_cnt['not found'] += 1
                ret.append({'url': site.get('url'), 'status': 'not found'})
                update_site_status(site.get('product_site_id'))
                LOGGER.info('[RESULT] price not found')
                continue
            else:
                all_found = []
                if tag_pattern_results and magic_result:
                    results.extend(tag_pattern_results)
                    for mr in magic_result:
                        for r in results:
                            if r.get('price') == mr.get('price'):
                                r['rule']['weight'] += mr.get('rule').get('weight')
                                r['currency'] = r['currency'] if r['currency'] else mr['currency']
                                r['method'] += ' + magic'
                                r['rule']['selector'] += ' + magic'
                    for r in tag_pattern_results:
                        all_found.append({
                            'rule': r.get('rule'),
                            'price': r.get('price'),
                            'currency': r.get('currency')
                        })
                    for r in magic_result:
                        all_found.append({
                            'rule': r.get('rule'),
                            'price': r.get('price'),
                            'currency': r.get('currency')
                        })
                else:
                    results.extend(tag_pattern_results if tag_pattern_results else magic_result)
                    for r in results:
                        all_found.append({
                            'rule': r.get('rule'),
                            'price': r.get('price'),
                            'currency': r.get('currency')
                        })

                results.sort(key=lambda x: float(x.get('rule').get('weight')), reverse=True)
                best_result = results[0]
                try:
                    LOGGER.info('[RESULT] ' + str(best_result.get('rule'))
                                + ' ' + str(best_result.get('currency')) + ' ' + str(best_result.get('price')))
                except Exception as e:
                    LOGGER.error(str(e))
                result_cnt[best_result.get('method')] += 1
                event = {
                    'product_site_id': site.get('product_site_id'),
                    'event_time': best_result.get('event_time'),
                    'product_price': best_result.get('price'),
                    'currency': best_result.get('currency')
                }
                update_events(event)
                # snipping website
                if need_screenshot:
                    screenshot_name = os.path.join(config.SITE_SCREENSHOT_DIR, str(site.get('product_site_id')) + '.png')
                    if not os.path.exists(screenshot_name):
                        try:
                            snip_website(site.get('url'), screenshot_name)
                            LOGGER.info('[SUCCESS] snipping website')
                        except Exception as e:
                            LOGGER.warning('snipping: ' + str(e))
                ret.append({
                    'url': site.get('url'),
                    'status': best_result.get('method'),
                    'price': best_result.get('price'),
                    'currency': best_result.get('currency'),
                    'rule': best_result.get('rule'),
                    'all': all_found
                })
                update_site_status(site.get('product_site_id'))
        except Exception as e:
            update_site_status(site.get('product_site_id'))
            LOGGER.error('get price: ' + str(e))

    print('\n=====================================================================')
    print('all:', str(result_cnt.get('all')))
    print('microdata:', str(result_cnt.get('microdata')))
    print('crawl error:', str(result_cnt.get('crawl error')))
    print('not found:', str(result_cnt.get('not found')))
    print('url pattern:', str(result_cnt.get('url pattern')))
    print('tag pattern:', str(result_cnt.get('tag pattern')))
    print('magic:', str(result_cnt.get('magic')))
    print('tag pattern + magic:', str(result_cnt.get('tag pattern + magic')))
    print('=====================================================================\n')

    LOGGER.info('=====================================================================')
    LOGGER.info('all: ' + str(result_cnt.get('all')))
    LOGGER.info('microdata: ' + str(result_cnt.get('microdata')))
    LOGGER.info('crawl error: ' + str(result_cnt.get('crawl error')))
    LOGGER.info('not found: ' + str(result_cnt.get('not found')))
    LOGGER.info('url pattern: ' + str(result_cnt.get('url pattern')))
    LOGGER.info('tag pattern: ' + str(result_cnt.get('tag pattern')))
    LOGGER.info('magic: ' + str(result_cnt.get('magic')))
    LOGGER.info('tag pattern + magic: ' + str(result_cnt.get('tag pattern + magic')))
    LOGGER.info('=====================================================================')

    print(ret)

    return ret


def get_price_only_by_magic(product_id):
    """
    main analyse operation
    :param product_id: product id
    :return: [{'url', 'status', 'rule', 'price', 'currency', 'all': {'rule', 'price', 'currency'}}, ...]
    """
    result_cnt = {
        'all': 0,
        'crawl error': 0,
        'not found': 0,
        'magic': 0
    }

    # get all sites
    sites = get_sites(product_id)
    image_urls = get_image_urls(product_id)
    all_data = {'sites': sites, 'image_urls': image_urls}
    result_cnt['all'] += len(sites)
    LOGGER.info('# %d => %d found' % (product_id, len(sites)))

    for site in all_data.get('sites'):
        print(site.get('url'))
        LOGGER.info(str(site.get('url')))
        # crawl raw data
        try:
            if not crawl_data(site.get('url'), site.get('site_id'), max_retry_times=3):
                result_cnt['crawl error'] += 1
                LOGGER.warning('failed to crawl data')
                continue
            else:
                LOGGER.info('[SUCCESS] crawl data')

            magic_result = magic_analyzer(site, all_data.get('image_urls'))
            if not magic_result:
                # price not found
                result_cnt['not found'] += 1
                LOGGER.info('[RESULT] price not found')
                continue
            else:
                best_result = magic_result[0]
                try:
                    LOGGER.info('[RESULT] ' + str(best_result.get('rule'))
                                + ' ' + str(best_result.get('currency')) + ' ' + str(best_result.get('price')))
                except Exception as e:
                    LOGGER.error(str(e))
                result_cnt['magic'] += 1
        except Exception as e:
            LOGGER.error('get price: ' + str(e))

    print('\n=====================================================================')
    print('all:', str(result_cnt.get('all')))
    print('crawl error:', str(result_cnt.get('crawl error')))
    print('not found:', str(result_cnt.get('not found')))
    print('magic:', str(result_cnt.get('magic')))
    print('=====================================================================\n')

    LOGGER.info('=====================================================================')
    LOGGER.info('all: ' + str(result_cnt.get('all')))
    LOGGER.info('crawl error: ' + str(result_cnt.get('crawl error')))
    LOGGER.info('not found: ' + str(result_cnt.get('not found')))
    LOGGER.info('magic: ' + str(result_cnt.get('magic')))
    LOGGER.info('=====================================================================')
    return 'done'


def url_pattern_analyzer(url_profiles_path, site):
    """
    analyse url according to url profiles
    :param url_profiles_path: url profile json file path
    :param site: dict, {'site_id', 'product_site_id', 'url', 'product_name'}
    :return: {'method': 'url pattern', 'price', 'currency', 'rule': {'selector', 'weight'}, 'event_time'}
    """
    with open(url_profiles_path) as f:
        url_profiles = json.load(f)
    domain = get_site_domain(site.get('site_id'))
    if not domain:
        return None
    rule = url_profiles.get(domain)
    if not rule:
        LOGGER.info('[FAIL] url pattern: no rule matched')
        return None

    success_flag = False
    try:
        success_flag, price, currency, event_time = url_profile_parser.get_price(site, rule)
    except Exception as e:
        LOGGER.error('url pattern: ' + str(e))

    if success_flag:
        p = {
            'method': 'url pattern',
            'price': price,
            'currency': currency,
            'event_time': event_time,
            'rule': {'selector': domain, 'weight': 2.0}
        }
        LOGGER.info('[SUCCESS] url pattern: ' + str(p))
        LOGGER.info('[RESULT] ' + str(p.get('currency')) + ' ' + str(p.get('price')))
    else:
        LOGGER.info('[FAIL] url pattern: price not found')
    return p if success_flag else None


def tag_pattern_analyzer(selector_path, site):
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
        error_flag, ret = tag_parser.get_price(site, tag_selectors)
    except Exception as e:
        LOGGER.error(str(e))
    return error_flag, ret


def magic_analyzer(site, image_urls):
    """
    analyse url in some magic ways, such as ML
    :param site: dict, {'site_id', 'product_site_id', 'url', 'product_name'}
    :param image_urls: list
    :return: [{'method': 'url pattern', 'price', 'currency', 'rule': {'selector', 'weight'}, 'event_time'}]
    """
    if not check_site_by_id(site.get('site_id')):
        return None

    try:
        res = MagicHayStack.get_price(site.get('url'), image_urls)
    except Exception as e:
        LOGGER.error(str(e))

    if not res:
        LOGGER.info('[FAIL] magic: price not found')
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
            LOGGER.info('[FAIL] magic: price not found')
            return None
        else:
            LOGGER.info('[SUCCESS] magic: ' + str(p))
            return p
