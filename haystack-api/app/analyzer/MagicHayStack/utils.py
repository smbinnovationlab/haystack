import time
import logging
import numpy as np
from collections import Counter


def cluster_score(cluster, confidence, truth, verbose=True):
    """
    Calculate cluster based score as 'Labeling max confidence instance in the cluster as 1' in binary classification
    :param cluster: [any], cluster each instance belonging to
    :param confidence: [float], confidence on each instance being True
    :param truth: [any], the true label for each instance
    """
    ret = []
    ranks = []
    count = 0
    s = set(cluster)
    for c in s:
        index = cluster == c
        x = confidence[index]
        y = truth[index]
        if not any(y == 1):
            continue

        count += 1
        choice = np.max(x) == x
        ret.append(np.count_nonzero(y[choice] == 1) / len(choice))

        sort = np.argsort(-x)
        ranks.append(np.mean(sort[y == 1]) / len(x))

    score = np.sum(ret) / float(count)
    if verbose:
        print('[Choose MAX] %g%% TP/P in %d cluster' % (score * 100, count))
        print(ranks)
        print('True labels on average rank %g%% in each cluster' % np.mean(ranks) * 100)
    return score


def timeit_dec(func):
    """ timeit decorator, need logging level as INFO """
    def wrapper(*args, **kwargs):
        tic = time.time()
        ret = func(*args, **kwargs)
        toc = time.time()
        logging.info('%s costs %gs' % (func.__name__, toc - tic))
        return ret
    return wrapper


def shuffle_split(X, y, ratio=0.9, dataframe=False):
    """
    Shuffle and split dataset by ratio
    :param X: numpy.array | pandas.DataFrame
    :param y: numpy.array | pandas.DataFrame
    :param ratio: float
    :param dataframe: bool, whether X, y are pandas.DataFrame
    :return: ((X_train, y_train), (X_test, y_test))
    """
    index = np.arange(len(X))
    np.random.shuffle(index)
    div = int(ratio * len(X))
    if dataframe:
        X = X.iloc
        y = y.iloc
    train = X[index[:div]], y[index[:div]]
    test = X[index[div:]], y[index[div:]]
    return train, test


def balanced_subset(X, y, dataframe=False):
    """ Sample balanced subset of data """
    c = Counter(y)
    _, count = c.most_common()[-1]      # least common label
    choice = []
    for k in c.keys():                  # take count samples from each
        index = np.where(y == k)[0]
        np.random.shuffle(index)
        choice.extend(index[:count])

    if dataframe:                       # dataframe requires special slice
        X = X.iloc
        y = y.iloc
    return X[choice], y[choice]


def augment_subset(X_df, y_df, label, level=2):
    """ Augment y == label by level times """
    c = Counter(y_df)
    _, count = c.most_common()[-1]  # least common label
    choice = []
    for k in c.keys():  # take count samples from each
        index = np.where(y_df == k)[0]
        np.random.shuffle(index)
        if k == label:
            choice.extend(index[:count].repeat(level))
        else:
            choice.extend(index[:int(count * level)])
    return X_df.iloc[choice], y_df.iloc[choice]


def calc_color_contrast(c1, c2, alpha=1.0):
    """
    https://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef
    :param c1: (r, g, b)
    :param c2: (r, g, b)
    :param alpha: alpha of c1 in front of c2
    :return: float, contrast
    """
    c1 = np.array(c1) / 255.0
    c2 = np.array(c2) / 255.0
    if alpha != 1:
        c1 = np.array(c1) * alpha + np.array(c2) * (1 - alpha)
    l1 = calc_luminance(c1)
    l2 = calc_luminance(c2)
    return (l1 + 0.05) / (l2 + 0.05)


def calc_luminance(c):
    """
    https://www.w3.org/TR/2008/REC-WCAG20-20081211/#relativeluminancedef
    :param c: (r, g, b)
    :return: float, luminance
    """
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def rgb_unpack(obj):
    """
    :param obj: selenium.webdriver.support.color.Color
    :return: (r, g, b), unpacked
    """
    return obj.red, obj.green, obj.blue


def _test_color_contrast():
    c2 = (40, 20, 90)
    c1 = (120, 30, 50)
    alpha = 0.3
    con = calc_color_contrast(c1, c2, alpha)
    # answer = 1.3
    print(con)


def _test_balance():
    X = np.array([[1], [2], [3], [4]])
    y = np.array([0, 1, 1, 1])
    print(balanced_subset(X, y))


def tmp_path():
    import os
    return os.path.join(os.getcwd(), 'tmp/')


def parse_price(s):
    """
    Parse s as price
    :param s: str
    :return: float
    """
    ret = -1.0
    s = s.strip().replace(' ', '')
    index = s.rfind(',')
    if index != -1:                 # find comma
        count = 0
        for i in range(index + 1, len(s)):
            if s[i].isdigit():
                count += 1
            else:
                break
        if count == 0:              # comma as ending
            pass
        elif count <= 2:            # comma as decimal point: $19,99
            s = s[:index] + '.' + s[index + 1:]
    s = s.replace(',', '')          # comma for 3-digits separator
    try:
        ret = float(s)
    except ValueError:
        logging.warning('Parsing price error on ' + str(s))
    except Exception as e:
        logging.error(e)
    return ret


def _test_parse():
    for s in ['2.34', '124 235.4', '132,234,13\n', 'adsv']:
        print(parse_price(s))


if __name__ == '__main__':
    # _test_color_contrast()
    # _test_balance()
    _test_parse()
