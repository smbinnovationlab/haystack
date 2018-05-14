# -*- coding:utf-8 -*-

import os
import sys
sys.path.append('..' + os.path.sep)

from conf import config
import json
import os
import re
import statistics
import urllib.request


def get_exchange_rates():
    """
    get currency exchange rates
    api from "http://fixer.io/"
    :return: rates = {'base': base_currency, 'data': latest_date, 'rates': {currency: rate}}
    """
    # api_url = 'http://api.fixer.io/latest?base=USD'
    # try:
    #     response = urllib.handle_requests.urlopen(api_url, data=None)
    #     rates_str = response.read().decode('utf-8')
    #     with open(r'.\utils\currency_exchange_rates.txt', 'w') as f:
    #         f.write(rates_str)
    # except Exception as e:
    #     print(e)
    #     with open(r'.\utils\currency_exchange_rates.txt') as f:
    #         rates_str = f.readline()
    with open(os.path.join(config.RULE_DIR, 'currency_exchange_rates.json')) as f:
        rates = json.load(f)
    # with open(r'.\utils\currency_exchange_rates.txt') as f:
    #     rates_str = f.readline()
    # rates = eval(rates_str)
    return rates


def exchange_price_list(price_list, target_currency):
    """
    :param price_list: [{'price': price, 'currency': currency}, ...]
    :param target_currency:
    :return: list of exchanged price
    """
    exchanged_price_list = []
    rates = get_exchange_rates()
    for item in price_list:
        status = 'success'
        if item['currency'] == target_currency:
            exchanged_price_list.append({'status': status, 'value': item['price']})
        else:
            if item['currency'] == rates['base']:
                status = 'success'
                rate = rates['rates'][target_currency] if rates['rates'][target_currency] else 1
                exchanged_price = round(item['price'] * rate, 2)
            elif target_currency == rates['base']:
                if item['currency'] in rates['rates'].keys():
                    status = 'success'
                    counter_rate = rates['rates'][item['currency']]
                    rate = 1 / counter_rate
                    exchanged_price = round(item['price'] * rate, 2)
                else:
                    print('currency %s not found' % item['currency'])
                    status = 'fail'
                    exchanged_price = item['price']
            else:
                if item['currency'] in rates['rates'].keys() \
                        and target_currency in rates['rates'].keys():
                    status = 'success'
                    rate = rates['rates'][target_currency] / rates['rates'][item['currency']]
                    exchanged_price = round(item['price'] * rate, 2)
                else:
                    status = 'fail'
                    exchanged_price = item['price']
                    if not item['currency'] in rates['rates'].keys():
                        print('currency %s not found' % item['currency'])
                    if target_currency not in rates['rates'].keys():
                        print('currency %s not found' % target_currency)

            exchanged_price_list.append({'status': status, 'value': exchanged_price})

    return exchanged_price_list


def price_formatter(price):
    try:
        match = re.match(r'(\D*?)(\\r|\s)*(\\\w{3})*([^\d|\s|\\r]*)(\\r|\s)*([\d|,]+\.*\d{,2})', price)
        currency = match.group(4)
        price = match.group(6)
        price = re.compile(',').sub('', price)
        return price, currency
    except Exception as e:
        print(e)
        return None, None


def currency_formatter(currency_str):
    if not currency_str:
        return
    currency_str = currency_str.strip().upper()
    with open(os.path.join(config.RULE_DIR, 'currency_symbols.json')) as f:
        currency_mapper = json.load(f)
        try:
            currency_code = currency_mapper.get(currency_str)
            if currency_code and not isinstance(currency_code, list):
                return currency_code
            else:
                return currency_str
        except Exception as e:
            print(e)


def check_price(vendor_price, site_price):
    """
    check if site price is too high or too low than the vendor price
    :param vendor_price: vendor price
    :param site_price: actual price in site
    :return: 'high' / 'low' / 'normal'
    """
    compare = site_price / vendor_price
    if 1.4 <= compare < 7.5:
        return 'high'
    elif compare >= 7.5:
        return 'abnormal'
    elif 0.1 < compare <= 0.5:
        return 'low'
    elif compare <= 0.1:
        return 'abnormal'
    else:
        return 'normal'


def remove_outlier_price(price_list):
    if len(price_list) <= 1:
        return [p[0] for p in price_list]

    price_list = sorted(price_list, key=lambda p: p[1])
    mean_price = statistics.mean([p[1] for p in price_list])
    std_price = statistics.stdev([p[1] for p in price_list])
    lower = abs(mean_price - 2 * std_price)
    upper = abs(mean_price + 2 * std_price)

    non_outlier_price_list = []
    for price in price_list:
        if lower < price[1] < upper:
            non_outlier_price_list.append(price[0])
    return non_outlier_price_list
