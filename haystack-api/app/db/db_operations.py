# -*- coding:utf-8 -*-

import os
import sys
sys.path.append('..' + os.path.sep)
from conf import config
from db.mysql_conf import mysql_engine
from db.object_definition import ProductEvent, Site, Product
from sqlalchemy.orm import sessionmaker
from utils.price_operation import currency_formatter, exchange_price_list, remove_outlier_price
from utils.regex import url_regex
import json
import re


def get_product(product_id, debug=False, target_currency='USD'):
    with open(os.path.join(config.RULE_DIR, 'currency_symbols.json')) as f:
        currency_mapper = json.load(f)
    if not currency_mapper:
        print('[Error]: missing currency_symbols.json')
        return None

    engine = mysql_engine()
    db_session = sessionmaker(bind=engine)
    session = db_session()

    product = session.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        session.close()
        return {
            'status': 'completed',
            'results': []
        }
    elif product.is_searching == 1:
        session.close()
        return {
            'status': 'searching',
            'results': []
        }

    product_sites = session.query(Site).filter(Site.product_id == product_id).all()

    sites_count = len(product_sites)
    finished_sites_count = 0
    sites = []
    for product_site in product_sites:
        is_finished = product_site.is_finished
        if is_finished == 0:
            continue

        finished_sites_count += 1

        product_event = session.query(ProductEvent).filter(ProductEvent.site_id == product_site.site_id)\
            .order_by(ProductEvent.event_time.desc()).first()

        event_time = None
        product_currency = None
        product_price = None
        exchanged_currency = None
        exchanged_price = None

        if product_event and product_event.product_currency in currency_mapper.values():
            event_time = product_event.event_time
            product_currency = product_event.product_currency
            product_price = product_event.product_price
            exchanged_results = exchange_price_list(
                [{'price': product_price, 'currency': product_currency}],
                target_currency
            )
            exchanged_price = exchanged_results[0].get('value')
            exchanged_currency = target_currency \
                if exchanged_results[0].get('status') == 'success' \
                else product_currency

        if debug:
            sites.append({
                'id': str(product_site.site_id),
                'domain': product_site.domain,
                'url': product_site.full_url,
                'doc_price': {
                    'value': product_price,
                    'currency': product_currency
                },
                'target_price': {
                    'value': exchanged_price,
                    'currency': exchanged_currency
                },
                'crawl_time': event_time,
                'debug_info': json.loads(product_site.debug_info)
            })
        else:
            if not product_currency or not product_price or exchanged_currency != target_currency:
                continue
            else:
                sites.append({
                    'id': str(product_site.site_id),
                    'domain': product_site.domain,
                    'url': product_site.full_url,
                    'doc_price': {
                        'value': product_price,
                        'currency': product_currency
                    },
                    'target_price': {
                        'value': exchanged_price,
                        'currency': exchanged_currency
                    },
                    'crawl_time': event_time
                })
    if finished_sites_count == sites_count:
        status = 'completed'
    else:
        status = 'processing'

    product_info = {
        'status': status,
        'results': sites
    }

    # filter outliers
    l1 = [r.get('id') for r in product_info.get('results')]
    l2 = [r.get('target_price').get('value') for r in product_info.get('results')]
    filtered_list = remove_outlier_price(list(zip(l1, l2)))
    filtered_results = []
    for r in product_info.get('results'):
        if r.get('id') in filtered_list:
            filtered_results.append(r)
    product_info['results'] = filtered_results

    session.close()
    return product_info


def add_site(product_id, url):
    engine = mysql_engine()
    db_session = sessionmaker(bind=engine)
    session = db_session()

    ret = session.query(Site).filter(Site.full_url == url).filter(Site.product_id == product_id).first()
    if ret:
        site_id = ret.site_id
    else:
        pattern = re.compile(url_regex)
        url_match = pattern.match(url)
        domain = url_match.group(3)
        new_site = Site(domain=domain, full_url=url, product_id=product_id)
        session.add(new_site)
        session.flush()
        site_id = new_site.site_id
        session.commit()

    session.close()
    return site_id


def set_site_finished(site_id, debug_info):
    engine = mysql_engine()
    db_session = sessionmaker(bind=engine)
    session = db_session()
    session.query(Site).filter(Site.site_id == site_id).update({Site.is_finished: 1,
                                                                Site.debug_info: json.dumps(debug_info)})
    session.commit()
    session.close()


def get_site_domain(site_id):
    engine = mysql_engine()
    db_session = sessionmaker(bind=engine)
    session = db_session()
    ret = session.query(Site.domain).filter(Site.site_id == site_id).first()
    if not ret:
        return None
    domain = ret.domain
    session.close()
    return domain


def add_event(site_id, price, currency, event_time, status=None, event_type=None):
    engine = mysql_engine()
    db_session = sessionmaker(bind=engine)
    session = db_session()
    price = float('%.2f' % float(price))
    if len(str(currency)) > 20:
        currency = ''
    currency = currency_formatter(currency)
    new_event = ProductEvent(site_id=site_id,
                             product_price=price,
                             product_currency=currency,
                             product_status=status,
                             event_time=event_time,
                             event_type=event_type)
    session.add(new_event)
    session.commit()
    session.close()


def add_product(product_id):
    engine = mysql_engine()
    db_session = sessionmaker(bind=engine)
    session = db_session()
    new_product = Product(product_id=product_id)
    session.add(new_product)
    session.commit()
    session.close()


def finish_product_searching(product_id):
    engine = mysql_engine()
    db_session = sessionmaker(bind=engine)
    session = db_session()
    session.query(Product).filter(Product.product_id == product_id).update({Product.is_searching: 0})
    session.commit()
    session.close()
