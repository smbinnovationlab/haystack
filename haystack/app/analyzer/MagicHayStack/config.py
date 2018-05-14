import os
import re
import logging
from .utils import tmp_path

INTERACTIVE = False

WEB_DRIVER_TIMEOUT = 15
CANDIDATES_NUMBER_THRESH = 32               # if exceeded, considered as collection page and rejected
PARALLEL_TIMEOUT = 120                      # timeout for each parallel job in pool
XPATH_RULE_SAMPLES = ["//*[(contains(@*,'price') or contains(@*, 'Price')) and string-length(text()) > 0]"]
REGEX_CACHE = {
    'currency': re.compile(r'(?:(?:CN|CNY|US|Fr|SG|EUR|JP|JPY)D?|[$\uFE69\uFF04￥€元円£￠￡¥฿]|\s)+', flags=re.IGNORECASE),
    'num': re.compile(r'\d+'),
    'non-price': re.compile(r'[%]]'),

    # float format price
    'money': re.compile(r'(?<![\d.])([\d,]+\.\d{2,3})(?![\d.])'),       # no more digit
    # comma float format price
    'money_comma': re.compile(r'\d{1,3}(?:,\d{2,3})+'),
    # currency prefix
    'money_pre': re.compile(r'(?:(?:CN|CNY|US|Fr|SG|EUR|JP|JPY)D?|[$\uFE69\uFF04￥€元£￠￡¥฿])\s*(\d+)'),
    # currency suffix
    'money_suf': re.compile(r'(\d+)\s*[元円]'),
}


def _rel_path(p):
    """ Convert to relative path to this file """
    return os.path.join(os.path.dirname(__file__), p)


DATA_SAVE_FILE = _rel_path("data/training_6.csv")
IMG_URLS_FILE = _rel_path('data/iuf[1].txt')
PAGE_URLS_FILE = _rel_path('data/puf[1].txt')
RECORD_FILE = _rel_path('data/record.csv')

FEATURE_COL_NAMES = ['font_size', 'x_pct', 'y_pct', 'contrast', 'luminance', 'dx', 'dy', 'dxy',
                     'r', 'g', 'b', 'currency', 'class']

MODEL_PICKLE_FILE = _rel_path('tmp/model.pkl')


def GET_WEB_DRIVER():
    from selenium import webdriver
    # driver = webdriver.Chrome()

    # driver.implicitly_wait(50)
    # driver.set_page_load_timeout(50)

    # for Windows, set executable_path to the path of phantomjs.exe
    executable_path = r'C:\Users\i332584\Workspace\Software\phantomjs-2.1.1-windows\bin\phantomjs.exe'
    driver = webdriver.PhantomJS(executable_path=executable_path)
    # for Linux, install phantomjs and it does not require executable_path
    # driver = webdriver.PhantomJS()

    return driver
