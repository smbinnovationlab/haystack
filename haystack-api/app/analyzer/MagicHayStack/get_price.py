# -*- coding:utf-8 -*-

import re
import os
import logging
from selenium import webdriver
import numpy as np
from sklearn.externals import joblib

from analyzer.MagicHayStack import config
from analyzer.MagicHayStack.data_generation import access_url
from analyzer.MagicHayStack.utils import timeit_dec, parse_price


@timeit_dec
def get_price(url, image_urls, record=None):
    """
    Outgoing API for price extraction
    :param url: str
    :param image_urls: [str]
    :param record: if need to be record, give a file name
    :return: [(price:str, currency:str, weight:float)] | [('', '', 0)]
    """
    # feature extraction
    driver = config.GET_WEB_DRIVER()
    _, texts, mat, img_found = access_url(driver, url, image_urls)
    if texts is None:
        driver.close()
        return []
    driver.close()

    # TODO:
    # mat[mat == -1] = 1e5

    # refuse if too many (might be listing page)
    if not img_found and len(texts) > config.CANDIDATES_NUMBER_THRESH:
        logging.warning('REJECT with image not found and %d candidates at %s' % (len(texts), url))
        return []

    if record:
        record_data(filename=record, url=url, texts=texts, mat=mat)

    # ML evaluation
    clf = joblib.load(config.MODEL_PICKLE_FILE)
    prob = clf.predict_proba(mat)
    p = prob[:, 1]                                                      # confidence of positive
    logging.info(texts)
    index_list = np.where(p == max(p))[0]                               # most confident ones
    ret = reformat_ret(texts=texts, p=p, index_list=index_list)         # to [(price, currency, confidence)] format

    # sort by texts for order-preserving
    seq = np.argsort([r[0] for r in ret])
    ret = [ret[i] for i in seq]
    ret = list(filter(trim_zero_price, ret))
    return ret


def reformat_ret(texts, p, index_list):
    """
    Helper function formating result of get_price
    :param texts: [str,]
    :param p: [float,]
    :param index_list: [int|float,]
    :return:
    """
    ret_val = []
    for index in index_list:
        index = int(index)
        pri, cur = separate_currency(texts[index])
        if pri is None:
            continue
        cur_val = (pri, cur, p[index])
        ret_val.append(cur_val)
    ret_val = list(set(ret_val))
    return ret_val


def record_data(filename, url, texts, mat, label=None):
    """
    Record unlabelled features for possible use
    :param filename: target record file name
    :param url: url accessed
    :param texts: text content of element
    :param mat: feature mat [font_size,x_pct,y_pct,contrast,luminance,dx,dy,dxy,r,g,b,currency]
    :param label: [{0,1}, ], optional, whether is true
    :return: None
    """
    if not os.path.isfile(filename):
        f = open(filename, 'w')
        f.write('url,font_size,x_pct,y_pct,contrast,luminance,dx,dy,dxy,r,g,b,currency,text,class\n')
    else:
        f = open(filename, 'a')
    if label is None:
        label  = [None] * len(texts)
    for t, row, l in zip(texts, mat, label):
        f.write(url + ',')
        for data in row:
            f.write(str(data) + ',')
        f.write(t.replace(',', '').replace('\n', ''))
        if l is None:
            f.write(',')
        else:
            f.write(',' + str(l))
        f.write('\n')
    f.close()


def trim_zero_price(ret_tuple):
    """
    Filtering function for removing zero price in get_price return value
    :param ret_tuple: seen in get_price
    :return:
    """
    return parse_price(ret_tuple[0]) != 0


def separate_currency(text):
    reg = ['money', 'money_pre', 'money_suf', 'money_comma']
    price = []
    for r in reg:
        price = config.REGEX_CACHE[r].findall(text)
        if len(price) != 0:
            continue
    if len(price) == 0:
        return None, None
    price = price[0]
    c = re.findall(config.REGEX_CACHE['currency'], str(text))
    if len(c) == 0:
        currency = ''
    else:
        currency = c[0].replace(' ', '')
    return price, currency


def submit_label(true_price, url, image_urls=None, record_file='tmp/submitted.csv'):
    """
    Submit price labeled for page_url
    :param true_price: float
    :param url: str
    :param image_urls:[str,]
    :param record_file: record file name
    :return:
    """
    if image_urls is None:
        image_urls = ['']
    driver = config.GET_WEB_DRIVER()
    _, texts, mat, img_found = access_url(driver, url, image_urls)
    if texts is None:
        driver.close()
        return
    driver.close()

    # label price close enough to true_price as 1
    price_texts = [separate_currency(t)[0] for t in texts]      # as str
    prices = np.array(list(map(parse_price, price_texts)))      # as float
    index = np.where(np.abs(prices - true_price) < 1.1)[0]      # close matches
    if len(index) == 0:
        logging.warning('No close price match found %g : %s' % (true_price, str(prices)))
        return
    label = np.zeros(len(texts), dtype=np.int)
    label[index] = 1

    record_data(filename=record_file, url=url, texts=texts, mat=mat, label=label)


def _test():
    # logging.basicConfig(level=logging.INFO)
    logging.basicConfig(level=logging.ERROR)
    # image_urls = list(map(str.strip, open('data/iuf.txt', 'r').readlines()))
    image_urls = ['a.jpg']
    # page_urls = list(map(str.strip, open('data/puf.txt', 'r').readlines()))
    page_urls = ['https://www.shopdecor.com/alessi-psjs-juicy-salif-squeezer-white.html']
    submit_label(50.01, page_urls[0], image_urls)
    # for u in page_urls:
    #     ret = get_price(u, image_urls, config.RECORD_FILE)
    #     print(ret)


# if __name__ == '__main__':
    # _test()
