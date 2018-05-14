# -*- coding:utf-8 -*-

import os
import sys
sys.path.append('..' + os.path.sep)

from conf import config
from db.mysql_conf import mysql_engine
from db.object_definition import ProductEvent, ProductSite, Site, VendorProduct, ProductImageUrl, ProductEventBak
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from utils.date_operation import generate_random_date
from utils.price_operation import exchange_price_list, check_price, currency_formatter
from utils.regex import url_regex
import datetime
import json
import os
import random
import re


def update_events(event):
    """
    add or update in DB(haystack/product_event)
    :param event: dict, {'product_site_id', 'event_time', 'product_price', 'currency'}
    """
    engine = mysql_engine()
    db_session = sessionmaker(bind=engine)
    session = db_session()

    product_price = float('%.2f' % float(event.get('product_price')))
    currency = event.get('currency')
    if len(str(currency)) > 20:
        currency = ''
    currency = currency_formatter(currency)
    product_site_id = event.get('product_site_id')
    event_time = event.get('event_time')

    exist_events = session.query(ProductEvent).filter(
        ProductEvent.product_site_id == product_site_id
    ).order_by(ProductEvent.event_time.asc()).all()

    need_to_save = True
    event_type = 'update'
    price_change = 1
    if not exist_events:
        event_type = 'add'
    else:
        for i in range(len(exist_events)):
            if exist_events[i].product_price == product_price:
                price_change = 0
                if exist_events[i].event_time.strftime('%Y-%m-%d %H:%M:%S') == event_time:
                    need_to_save = False
                    break
                else:
                    if event_time < exist_events[i].event_time.strftime('%Y-%m-%d %H:%M:%S') and i == 0:
                        event_type = 'add'
                        session.query(ProductEvent).filter(
                            ProductEvent.event_id == exist_events[i].event_id
                        ).update({ProductEvent.event_type: 'update', ProductEvent.price_change: 0})
                        session.commit()
                        break
            else:
                price_change = 1
                if exist_events[i].event_time.strftime('%Y-%m-%d %H:%M:%S') == event_time:
                    need_to_save = False
                    session.query(ProductEvent).filter(
                        ProductEvent.event_id == exist_events[i].event_id
                    ).update({ProductEvent.product_price: product_price})
                    if i > 0:
                        previous_price = session.query(ProductEvent.product_price)\
                            .filter(ProductEvent.event_id == exist_events[i - 1].event_id)
                        session.query(ProductEvent).filter(ProductEvent.event_id == exist_events[i - 1].event_id)\
                            .update({ProductEvent.price_change: (1 if product_price != previous_price else 0)})
                    if i < len(exist_events) - 1:
                        next_price = session.query(ProductEvent.product_price)\
                            .filter(ProductEvent.event_id == exist_events[i + 1].event_id)
                        session.query(ProductEvent).filter(ProductEvent.event_id == exist_events[i + 1].event_id)\
                            .update({ProductEvent.price_change: (1 if product_price != next_price else 0)})
                    session.commit()
                    break
                else:
                    if event_time < exist_events[i].event_time.strftime('%Y-%m-%d %H:%M:%S') and i == 0:
                        event_type = 'add'
                        session.query(ProductEvent).filter(ProductEvent.event_id == exist_events[i].event_id)\
                            .update({ProductEvent.event_type: 'update'})
                        session.commit()
                        break

    if need_to_save:
        # Save to DB
        new_product_event = ProductEvent(
            product_site_id=product_site_id,
            event_time=event_time,
            event_type=event_type,
            product_price=product_price,
            currency=currency,
            price_change=price_change
        )
        session.add(new_product_event)
        session.commit()

    session.close()


def get_events():
    """
    get events
    :return: events ordered by time
             [{'event_id', 'product_site_id', 'event_time', 'product_price', 'product_price_compare',
               'currency', 'event_type', 'domain', 'full_url', 'product_id', 'product_name'}, ...]
    """
    with open(os.path.join(config.RULE_DIR, 'currency_symbols.json')) as f:
        currency_mapper = json.load(f)
    if not currency_mapper:
        print('[Error]: missing currency_symbols.json')
        return

    engine = mysql_engine()
    db_session = sessionmaker(bind=engine)
    session = db_session()

    ret_events = session.query(ProductEvent, ProductSite).filter(
        ProductEvent.product_site_id == ProductSite.product_site_id
    ).order_by(ProductEvent.event_time.desc()).all()

    events = []
    if not ret_events:
        return events
    for e in ret_events:
        if e.ProductEvent.currency not in currency_mapper.values():
            continue

        c_site_id = e.ProductSite.site_id
        c_product_id = e.ProductSite.product_id
        c_site = session.query(Site).filter(Site.site_id == c_site_id).first()
        c_vendor_product = session.query(VendorProduct).filter(VendorProduct.product_id == c_product_id).first()
        if c_vendor_product.is_new == -1:
            continue

        temp_price_list = [{
            'price': e.ProductEvent.product_price,
            'currency': e.ProductEvent.currency
        }]
        exchanged_price = exchange_price_list(temp_price_list, c_vendor_product.currency)
        exchanged_price = exchanged_price[0]
        product_price_compare = check_price(c_vendor_product.product_price, exchanged_price)
        if product_price_compare == 'abnormal':
            continue
        event = {
            'event_id': e.ProductEvent.event_id,
            'product_site_id': e.ProductEvent.product_site_id,
            'event_time': e.ProductEvent.event_time,
            'product_price': e.ProductEvent.product_price,
            'product_price_compare': product_price_compare,
            'currency': e.ProductEvent.currency,
            'event_type': e.ProductEvent.event_type,
            'price_change': e.ProductEvent.price_change,
            'domain': c_site.domain,
            'full_url': c_site.full_url,
            'product_id': c_product_id,
            'product_name': c_vendor_product.product_name
        }
        events.append(event)

    session.close()
    return events


def get_vendor_product(product_id=-1):
    """
    get vendor products
    :param product_id: get product according to product_id. if default -1, get all products
    :return: vendor products information
             [{'product_id', 'product_name', 'currency', 'vendor_price',
               'max_price', 'min_price', 'avg_price', 'is_favourite',
               'events': {
                    'event_id', 'product_site_id', 'event_type', 'event_time',
                    'product_price', 'product_price_compare', 'currency', 'domain', 'full_url'
               }
             }]
    """
    with open(os.path.join(config.RULE_DIR, 'currency_symbols.json')) as f:
        currency_mapper = json.load(f)
    if not currency_mapper:
        print('[Error]: missing currency_symbols.json')
        return

    engine = mysql_engine()
    db_session = sessionmaker(bind=engine)
    session = db_session()

    if product_id == -1:
        ret_products = session.query(VendorProduct, ProductSite).filter(
            ProductSite.product_id == VendorProduct.product_id
        ).order_by(ProductSite.product_id).all()
    else:
        ret_products = session.query(VendorProduct, ProductSite).filter(
            VendorProduct.product_id == product_id
        ).filter(
            ProductSite.product_id == VendorProduct.product_id
        ).order_by(ProductSite.product_id).all()

    vendor_products = []
    if not ret_products:
        return vendor_products

    i = 0
    while i < len(ret_products):
        if ret_products[i].VendorProduct.is_new == -1:
            i += 1
            continue
        c_product_id = ret_products[i].VendorProduct.product_id
        c_product_name = ret_products[i].VendorProduct.product_name
        c_vendor_price = ret_products[i].VendorProduct.product_price
        c_currency = ret_products[i].VendorProduct.currency
        c_is_favourite = ret_products[i].VendorProduct.is_favourite
        c_sku_id = ret_products[i].VendorProduct.sku_id

        price_list = []
        event_list = []
        while (i < len(ret_products)
               and ret_products[i].VendorProduct.product_id == c_product_id):
            c_product_site_id = ret_products[i].ProductSite.product_site_id
            ret_events = session.query(ProductEvent, ProductSite, Site).filter(
                ProductEvent.product_site_id == ProductSite.product_site_id
            ).filter(
                ProductSite.site_id == Site.site_id
            ).filter(
                ProductEvent.product_site_id == c_product_site_id
            ).all()

            for e in ret_events:
                if e.ProductEvent.currency not in currency_mapper.values():
                    continue

                temp_price_list = [{
                    'price': e.ProductEvent.product_price,
                    'currency': e.ProductEvent.currency
                }]
                exchanged_price = exchange_price_list(temp_price_list, c_currency)
                exchanged_price = exchanged_price[0]
                product_price_compare = check_price(c_vendor_price, exchanged_price)
                if product_price_compare == 'abnormal':
                    continue

                temp = {
                    'price': e.ProductEvent.product_price,
                    'currency': e.ProductEvent.currency
                }
                price_list.append(temp)
                event_list.append(e)
            i += 1

        if len(price_list) > 0:
            exchanged_price_list = exchange_price_list(price_list, c_currency)
            max_price = min_price = exchanged_price_list[0]
            sum_price = 0
            for p in exchanged_price_list:
                if p > max_price:
                    max_price = p
                if p < min_price:
                    min_price = p
                sum_price += p
            avg_price = round(sum_price / len(price_list), 2)
        else:
            max_price = min_price = avg_price = 0

        event_list.sort(key=lambda obj: obj.ProductEvent.event_time, reverse=True)
        events = []
        for e in event_list:
            temp_price_list = [{
                'price': e.ProductEvent.product_price,
                'currency': e.ProductEvent.currency
            }]
            exchanged_price = exchange_price_list(temp_price_list, c_currency)
            exchanged_price = exchanged_price[0]
            product_price_compare = check_price(c_vendor_price, exchanged_price)
            event = {
                'event_id': e.ProductEvent.event_id,
                'product_site_id': e.ProductEvent.product_site_id,
                'event_type': e.ProductEvent.event_type,
                'event_time': e.ProductEvent.event_time,
                'price_change': e.ProductEvent.price_change,
                'product_price': e.ProductEvent.product_price,
                'exchanged_price': exchanged_price,
                'product_price_compare': product_price_compare,
                'currency': e.ProductEvent.currency,
                'domain': e.Site.domain,
                'full_url': e.Site.full_url
            }
            events.append(event)

        avg_price_compare = check_price(c_vendor_price, avg_price)
        sites_count, finished_sites_count = get_status(c_product_id)
        vendor_product = {
            'product_id': c_product_id,
            'product_name': c_product_name,
            'currency': c_currency,
            'vendor_price': c_vendor_price,
            'sku_id': c_sku_id,
            'max_price': max_price,
            'min_price': min_price,
            'avg_price': avg_price,
            'avg_price_compare': avg_price_compare,
            'is_favourite': c_is_favourite,
            'events': events,
            'sites_count': sites_count,
            'finished_sites_count': finished_sites_count
        }
        vendor_products.append(vendor_product)

    session.close()
    return vendor_products


def add_vendor_product(name, price, currency, sku_id, unknown=False):
    """
    add vendor product information to DB(haystack/vendor_product)
    :return: 'success'
    """
    engine = mysql_engine()
    db_session = sessionmaker(bind=engine)
    session = db_session()

    if not unknown:
        is_exist = True if get_product_id(sku_id) else False
        if not is_exist:
            new_product = VendorProduct(product_name=name, product_price=price, currency=currency, sku_id=sku_id)
            session.add(new_product)
            session.commit()
    else:
        new_product = VendorProduct(product_name='unknown', product_price=0.00, is_new=-1, sku_id=sku_id)
        session.add(new_product)
        session.flush()
        new_product_id = new_product.product_id
        session.commit()

    session.close()
    return new_product_id


def get_product_site(product_site_id, event_id=-1):
    """
    get product sites
    :param product_site_id: product_site_id
    :param event_id: get event according to event_id. if default -1, get all events
    """
    with open(os.path.join(config.RULE_DIR, 'currency_symbols.json')) as f:
        currency_mapper = json.load(f)
    if not currency_mapper:
        print('[Error]: missing currency_symbols.json')
        return

    engine = mysql_engine()
    db_session = sessionmaker(bind=engine)
    session = db_session()

    ret = session.query(ProductSite, Site, VendorProduct).filter(
        ProductSite.site_id == Site.site_id
    ).filter(
        ProductSite.product_site_id == ProductEvent.product_site_id
    ).filter(
        ProductSite.product_id == VendorProduct.product_id
    ).filter(
        ProductSite.product_site_id == product_site_id
    ).first()

    c_domain = ret.Site.domain
    c_full_url = ret.Site.full_url
    c_country = ret.Site.country
    c_site_type = ret.Site.site_type
    c_last_indexed = ret.Site.last_indexed
    c_product_id = ret.VendorProduct.product_id
    c_product_name = ret.VendorProduct.product_name
    c_vendor_price = ret.VendorProduct.product_price
    c_currency = ret.VendorProduct.currency

    ret_events = session.query(
        ProductSite, ProductEvent
    ).filter(
        ProductEvent.product_site_id == ProductSite.product_site_id
    ).filter(
        ProductSite.product_site_id == product_site_id
    ).order_by(
        ProductEvent.event_time.desc()
    ).all()

    events = []

    c_event_time = None
    c_product_status = None
    get_current_price = False
    c_price = -1
    c_price_compare = 'normal'
    for ret_event in ret_events:
        if ret_event.ProductEvent.currency not in currency_mapper.values():
            continue
        temp_price_list = [{
            'price': ret_event.ProductEvent.product_price,
            'currency': ret_event.ProductEvent.currency
        }]
        exchanged_price = exchange_price_list(temp_price_list, c_currency)
        exchanged_price = exchanged_price[0]
        product_price_compare = check_price(c_vendor_price, exchanged_price)
        if product_price_compare == 'abnormal':
            continue
        event = {
            'event_id': ret_event.ProductEvent.event_id,
            'event_type': ret_event.ProductEvent.event_type,
            'event_time': ret_event.ProductEvent.event_time,
            'product_price': exchanged_price,
            'product_price_compare': product_price_compare,
            'price_change': ret_event.ProductEvent.price_change,
        }
        events.append(event)

        if str(event_id) == str(-1) and not get_current_price:
            c_price = exchanged_price
            c_price_compare = product_price_compare
            c_event_time = ret_event.ProductEvent.event_time
            c_product_status = ret_event.ProductEvent.product_status
            get_current_price = True

        if str(event_id) != str(-1) and not get_current_price:
            if str(ret_event.ProductEvent.event_id) == str(event_id):
                c_price = exchanged_price
                c_price_compare = product_price_compare
                c_event_time = ret_event.ProductEvent.event_time
                c_product_status = ret_event.ProductEvent.product_status
                get_current_price = True

    product_site_info = {
        'product_site_id': product_site_id,
        'domain': c_domain,
        'full_url': c_full_url,
        'country': c_country,
        'site_type': c_site_type,
        'last_indexed': c_last_indexed,
        'product_id': c_product_id,
        'product_name': c_product_name,
        'current_price': c_price,
        'current_price_compare': c_price_compare,
        'current_event_time': c_event_time,
        'current_product_status': c_product_status,
        'currency': c_currency,
        'events': events
    }

    session.close()
    return product_site_info


def add_to_favourites(product_id):
    """
    :return: 'success' / 'fail'
    """
    engine = mysql_engine()
    db_session = sessionmaker(bind=engine)
    session = db_session()

    try:
        session.query(VendorProduct).filter(
            VendorProduct.product_id == product_id
        ).update({VendorProduct.is_favourite: 1})
        session.commit()
        session.close()
        status = "success"
    except Exception as e:
        print(e)
        session.close()
        status = "fail"

    return status


def remove_from_favourites(product_id):
    """
    :return: 'success' / 'fail'
    """
    engine = mysql_engine()
    db_session = sessionmaker(bind=engine)
    session = db_session()

    try:
        session.query(VendorProduct).filter(
            VendorProduct.product_id == product_id
        ).update({VendorProduct.is_favourite: 0})
        session.commit()
        session.close()
        status = "success"
    except Exception as e:
        print(e)
        session.close()
        status = "fail"

    return status


def check_site_by_id(site_id):
    engine = mysql_engine()
    db_session = sessionmaker(bind=engine)
    session = db_session()
    ret = session.query(Site.site_id).filter(Site.site_id == site_id).first()
    session.close()
    return ret is not None


def add_site(url, product_id):
    """
    parse domain, pattern_url, full_url from url
    :param url: url
    :param product_id: vendor product id
    :return: site_id
    """
    engine = mysql_engine()
    db_session = sessionmaker(bind=engine)
    session = db_session()

    # db/haystack/site
    ret = session.query(Site).filter(Site.full_url == url).first()
    if not ret:
        pattern = re.compile(url_regex)
        url_match = pattern.match(url)
        url_domain = url_match.group(3)
        new_site = Site(domain=url_domain, full_url=url)
        session.add(new_site)
        session.commit()
        ret = session.query(Site.site_id).filter(Site.full_url == url).first()
        site_id = ret.site_id
        # db/haystack/product_site
        new_product_site = ProductSite(product_id=product_id, site_id=site_id)
        session.add(new_product_site)
        session.commit()

    session.close()


def update_site(site_id, site_type, country):
    engine = mysql_engine()
    db_session = sessionmaker(bind=engine)
    session = db_session()
    session.query(Site).filter(
        Site.site_id == site_id
    ).update({Site.site_type: site_type, Site.country: country})
    session.commit()
    session.close()


def get_sites(product_id):
    engine = mysql_engine()
    db_session = sessionmaker(bind=engine)
    session = db_session()

    ret = session.query(VendorProduct.product_name).filter(VendorProduct.product_id == product_id).first()
    if not ret:
        return
    product_name = ret.product_name
    ret = session.query(ProductSite).filter(ProductSite.product_id == product_id).all()
    sites = []
    for r in ret:
        product_site_id = r.product_site_id
        site_id = r.site_id
        ret_site = session.query(Site.full_url).filter(Site.site_id == site_id).first()
        if not ret_site:
            continue
        url = ret_site.full_url
        site_info = {
            'site_id': site_id,
            'product_site_id': product_site_id,
            'url': url,
            'product_name': product_name
        }
        sites.append(site_info)
    session.close()
    return sites


def get_site_domain(site_id):
    """
    get domain from DB(haystack/site)
    """
    engine = mysql_engine()
    db_session = sessionmaker(bind=engine)
    session = db_session()

    ret = session.query(Site.domain).filter(Site.site_id == site_id).first()
    if not ret:
        return None
    domain = ret.domain
    session.close()
    return domain


def add_image_url(url, product_id):
    engine = mysql_engine()
    db_session = sessionmaker(bind=engine)
    session = db_session()

    # db/haystack/product_image_url
    ret = session.query(ProductImageUrl.image_id).filter(ProductImageUrl.image_url == url).first()
    if not ret:
        new_image_url = ProductImageUrl(image_url=url, product_id=product_id)
        session.add(new_image_url)
        session.commit()

    session.close()


def get_image_urls(product_id):
    engine = mysql_engine()
    db_session = sessionmaker(bind=engine)
    session = db_session()

    ret = session.query(ProductImageUrl).filter(ProductImageUrl.product_id == product_id).all()
    image_urls = []
    for r in ret:
        image_urls.append(r.image_url)
    session.close()
    return image_urls


def clear_db():
    engine = mysql_engine()
    db_session = sessionmaker(bind=engine)
    session = db_session()
    session.query(Site).delete()
    session.commit()
    session.query(VendorProduct).delete()
    session.commit()
    session.close()


def beautify_event_time():
    engine = mysql_engine()
    db_session = sessionmaker(bind=engine)
    session = db_session()

    all_events = session.query(ProductEvent).all()
    for event in all_events:
        ret = session.query(ProductEventBak).filter(ProductEventBak.event_id == event.event_id).first()
        if not ret:
            new_event_bak = ProductEventBak(
                event_id=event.event_id, product_site_id=event.product_site_id,
                event_time=event.event_time, event_type=event.event_type,
                product_name=event.product_name, product_price=event.product_price,
                currency=event.currency, product_status=event.product_status,
                price_change=event.price_change
            )
            session.add(new_event_bak)
    session.commit()

    ret = session.query(VendorProduct.product_id).all()
    for r in ret:
        product_id = r.product_id
        all_events = session.query(ProductSite, ProductEvent).filter(
            ProductEvent.product_site_id == ProductSite.product_site_id).filter(
            ProductSite.product_id == product_id).all()
        if not all_events:
            continue
        all_events_copy = all_events
        all_events_copy.sort(key=lambda obj: obj.ProductEvent.event_time, reverse=True)
        latest_event_time = all_events_copy[0].ProductEvent.event_time
        date_list = generate_random_date(str(latest_event_time), len(all_events))
        random.shuffle(date_list)
        new_data = list(zip(all_events, date_list))
        new_data.sort(key=lambda obj: obj[-1])

        exist_product_site_id = []
        for data in new_data:
            if data[0].ProductEvent.product_site_id not in exist_product_site_id:
                session.query(ProductEvent).filter(
                    ProductEvent.event_id == data[0].ProductEvent.event_id).update(
                    {ProductEvent.event_time: data[-1], ProductEvent.event_type: 'add'})
                session.commit()
                exist_product_site_id.append(data[0].ProductEvent.product_site_id)
            else:
                session.query(ProductEvent).filter(
                    ProductEvent.event_id == data[0].ProductEvent.event_id).update(
                    {ProductEvent.event_time: data[-1], ProductEvent.event_type: 'update'})
                session.commit()

    session.close()


def modify_event_time_up_to_date(host, password):
    engine = create_engine('mysql+pymysql://root:%s@%s:3306/haystack?charset=utf8mb4'
                           % (password, host))
    db_session = sessionmaker(bind=engine)
    session = db_session()

    ret = session.query(func.max(ProductEvent.event_time).label('latest_date')).first()
    latest_date = ret.latest_date

    current_date = datetime.datetime.now()
    delay_days = (current_date - latest_date).days - 1

    all_events = session.query(ProductEvent.event_id, ProductEvent.event_time).all()

    for i, event in enumerate(all_events):
        event_id = event.event_id
        event_time = event.event_time
        new_event_time = event_time + datetime.timedelta(days=delay_days)
        new_event_time_str = datetime.datetime.strftime(new_event_time, '%Y-%m-%d %H:%M:%S')

        session.query(ProductEvent).filter(ProductEvent.event_id == event_id)\
            .update({ProductEvent.event_time: new_event_time_str})
        session.commit()

    session.close()


def get_crawled_sites():
    engine = mysql_engine()
    db_session = sessionmaker(bind=engine)
    session = db_session()
    ret = session.query(Site).filter(Site.last_indexed.isnot(None))

    crawled_sites = []
    for r in ret:
        temp = session.query(ProductSite.product_id).filter(ProductSite.site_id == r.site_id).first()
        temp = session.query(VendorProduct.is_new).filter(VendorProduct.product_id == temp.product_id).first()
        if temp.is_new == -1:
            continue
        else:
            crawled_sites.append({
                'site_id': r.site_id,
                'domain': r.domain,
                'full_url': r.full_url,
                'last_indexed': r.last_indexed
            })
    session.close()
    return crawled_sites


def get_product_id(sku_id, new_only=False):
    engine = mysql_engine()
    db_session = sessionmaker(bind=engine)
    session = db_session()
    if not new_only:
        ret = session.query(VendorProduct).filter(VendorProduct.sku_id == sku_id).first()
    else:
        ret = session.query(VendorProduct).filter(VendorProduct.sku_id == sku_id)\
            .filter(VendorProduct.is_new == 1).first()
    session.close()
    if not ret:
        return None
    else:
        return ret.product_id


def get_status(product_id):
    engine = mysql_engine()
    db_session = sessionmaker(bind=engine)
    session = db_session()
    ret1 = session.query(func.count(Site.site_id).label('count'))\
        .select_from(Site, ProductSite).filter(ProductSite.site_id == Site.site_id)\
        .filter(ProductSite.product_id == product_id).first()
    ret2 = session.query(func.count(Site.site_id).label('count'))\
        .select_from(Site, ProductSite).filter(ProductSite.site_id == Site.site_id) \
        .filter(ProductSite.product_id == product_id).filter(Site.status == 1).first()
    return ret1.count, ret2.count


def update_site_status(product_site_id):
    engine = mysql_engine()
    db_session = sessionmaker(bind=engine)
    session = db_session()
    ret = session.query(ProductSite.site_id).filter(ProductSite.product_site_id == product_site_id).first()
    session.query(Site).filter(Site.site_id == ret.site_id).update({Site.status: 1})
    session.commit()
    session.close()


def update_product_status(product_id):
    engine = mysql_engine()
    db_session = sessionmaker(bind=engine)
    session = db_session()
    session.query(VendorProduct).filter(VendorProduct.product_id == product_id).update({VendorProduct.is_new: 0})
    session.commit()
    session.close()


def reset_site_status():
    engine = mysql_engine()
    db_session = sessionmaker(bind=engine)
    session = db_session()
    session.query(Site).update({Site.status: 0})
    session.commit()
    session.close()


def format_currency():
    engine = mysql_engine()
    db_session = sessionmaker(bind=engine)
    session = db_session()
    ret = session.query(ProductEvent)
    for r in ret:
        formatted_currency = currency_formatter(r.currency)
        session.query(ProductEvent).filter(ProductEvent.event_id == r.event_id)\
            .update({ProductEvent.currency: formatted_currency})
    session.commit()
    session.close()


def api_get_vendor_product(product_id):
    with open(os.path.join(config.RULE_DIR, 'currency_symbols.json')) as f:
        currency_mapper = json.load(f)
    if not currency_mapper:
        print('[Error]: missing currency_symbols.json')
        return

    engine = mysql_engine()
    db_session = sessionmaker(bind=engine)
    session = db_session()

    ret_products = session.query(VendorProduct, ProductSite)\
        .filter(VendorProduct.product_id == product_id)\
        .filter(ProductSite.product_id == VendorProduct.product_id)\
        .order_by(ProductSite.product_id).all()

    vendor_product = None
    if not ret_products:
        return vendor_product

    i = 0
    while i < len(ret_products):
        c_product_id = ret_products[i].VendorProduct.product_id
        c_product_name = ret_products[i].VendorProduct.product_name
        c_vendor_price = ret_products[i].VendorProduct.product_price
        c_currency = ret_products[i].VendorProduct.currency
        c_is_favourite = ret_products[i].VendorProduct.is_favourite
        c_sku_id = ret_products[i].VendorProduct.sku_id

        price_list = []
        event_list = []
        while i < len(ret_products) and ret_products[i].VendorProduct.product_id == c_product_id:
            c_product_site_id = ret_products[i].ProductSite.product_site_id
            ret_events = session.query(ProductEvent, ProductSite, Site)\
                .filter(ProductEvent.product_site_id == ProductSite.product_site_id)\
                .filter(ProductSite.site_id == Site.site_id)\
                .filter(ProductEvent.product_site_id == c_product_site_id).all()

            for e in ret_events:
                if e.ProductEvent.currency not in currency_mapper.values():
                    continue
                temp = {
                    'price': e.ProductEvent.product_price,
                    'currency': e.ProductEvent.currency
                }
                price_list.append(temp)
                event_list.append(e)
            i += 1

        event_list.sort(key=lambda obj: obj.ProductEvent.event_time, reverse=True)
        events = []
        for e in event_list:
            event = {
                'event_id': e.ProductEvent.event_id,
                'product_site_id': e.ProductEvent.product_site_id,
                'event_type': e.ProductEvent.event_type,
                'event_time': e.ProductEvent.event_time,
                'price_change': e.ProductEvent.price_change,
                'product_price': e.ProductEvent.product_price,
                'currency': e.ProductEvent.currency,
                'domain': e.Site.domain,
                'full_url': e.Site.full_url
            }
            events.append(event)

        sites_count, finished_sites_count = get_status(c_product_id)
        vendor_product = {
            'product_id': c_product_id,
            'product_name': c_product_name,
            'currency': c_currency,
            'vendor_price': c_vendor_price,
            'sku_id': c_sku_id,
            'is_favourite': c_is_favourite,
            'events': events,
            'sites_count': sites_count,
            'finished_sites_count': finished_sites_count
        }

    session.close()
    return vendor_product
