import numpy as np
import pandas as pds
from selenium import webdriver
from selenium.webdriver.support.color import Color
import argparse
import io
import sys
from bs4 import BeautifulSoup
# from google.cloud import vision
# from google.cloud.vision import types
#
from .data_generation import *
from .utils import *
#
# d = webdriver.Chrome('/Users/bh/tools/chromedriver')
# d.implicitly_wait(15)
# d.get('https://www.zalora.com.ph/anello-anello-backpack-grey-803520.html?utm_source=HasOffers&utm_medium=Affiliate&utm_campaign=%zp&utm_content={$src.ShortSKU}')
# img = d.find_element_by_id('prdImage')
#
# price = d.find_element_by_id('js-price')
#
# text_c = Color.from_string(price.value_of_css_property('color'))
# background_c = Color.from_string(price.value_of_css_property('background-color'))
#
# client = vision.ImageAnnotatorClient()
# d = \
#     {
#         'image': {
#             'source': {
#                 'image_uri': 'https://img14.360buyimg.com/n5/s450x450_jfs/t3190/9/6775176788/204588/cc8a9bd4/58abb8bfNe5fe2ce8.jpg'
#             }
#         },
#         'features': [{
#             'type': 'WEB_DETECTION',
#             'max_results': 50
#         }]
#     }
# response = client.annotate_image(d)


def exact_match():
    sys.path.append('/Users/bh/tools/')
    with open('data/iuf.txt', 'r') as f:
        img_urls = list(map(str.strip, f.readlines()))
    with open('data/puf.txt', 'r') as f:
        page_urls = list(map(str.strip, f.readlines()))
    for im, pg in zip(img_urls, page_urls):
        f = open('tmp/i.tmp', 'w')
        f.write(im)
        f.close()
        f = open('tmp/p.tmp', 'w')
        f.write(pg)
        f.close()
        interactive_labeling('tmp/p.tmp', 'tmp/i.tmp')


def bs_get_all_image_urls(bs=None, html=None):
    """
    Find urls of all image opened on a web page (Shortened) based on BeatufulSoup4. Need either argument
    :param bs: BeatufulSoup
    :param html: html text
    :return: [str], shortened url
    """
    if bs is None:
        bs = BeautifulSoup(html)
    imgs = bs.find_all(name='img')
    urls = [im['src'] for im in imgs]
    urls = shorten_image_urls(urls)
    return urls


def _test():
    df = pds.read_csv('data/mint.csv')
    cols = df.columns
    X = df[cols[1:-4]]
    y = df['class']
    clusters = list(set(df['url']))
    X_b, y_b = balanced_subset(X, y, dataframe=True)
    train, test = shuffle_split(X_b, y_b, dataframe=True)

    from sklearn.ensemble import AdaBoostClassifier
    from sklearn.tree import DecisionTreeClassifier
    abc = AdaBoostClassifier(base_estimator=DecisionTreeClassifier(max_depth=6), n_estimators=10)
    abc.fit(train[0], train[1])

    score = abc.score(test[0], test[1])
    print(abc.predict(test[0]))
    print(test[1])
    print('Test set ' + str(score))
    score = abc.score(X, y)
    print('Whole set ' + str(score))

    # other set
    df = pds.read_csv('data/perfect.csv')
    cols = df.columns
    X = df[cols[1:-4]]
    y = df['class']
    score = abc.score(X, y)
    print('Other set ' + str(score))

    pred = abc.predict(X)
    error = pred != y
    n_error = np.count_nonzero(error)
    c = np.count_nonzero(np.logical_and(error, X['dxy'] == -1))
    print('In other set, %g%% errors come along with image missing' % (c / float(n_error) * 100))

    # abc.fit(X, y)

    # url = clusters[np.random.randint(len(clusters))]
    # test_index = np.where(df['url'] == url)[0]
    # test = X.iloc[test_index], y.iloc[test_index]
    #
    # prob = abc.predict_proba(test[0])
    # pmax = prob[:, 1].argmax()
    # print(prob)
    # print(pmax)
    # print(np.where(test[1])[0])
    # pred = abc.predict()
    # print(pred)
    # print(test[1])
    # tp = np.count_nonzero(np.logical_and(pred == 1, test[1] == 1)) / float(np.count_nonzero(pred == 1))
    # print("True positive " + str(tp))
    # tn = np.count_nonzero(np.logical_and(pred == 0, test[1] == 0)) / float(np.count_nonzero(pred == 0))
    # print("True negative " + str(tn))





if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # exact_match()
    _test()

