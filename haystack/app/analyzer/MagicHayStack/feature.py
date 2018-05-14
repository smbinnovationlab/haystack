from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.color import Color

from . import config
from .utils import *


def find_price_by_rule(driver, xpath_rules, img_ele):
    """
    Find price in opened web page by xpath_rule, use img_ele as hint
    :param driver: selenium.webdriver
    :param xpath_rules: [str]
    :param img_ele: selenium
    :return: ([element], [[float]])
    """
    candidates = set()

    for rule in xpath_rules:  # apply each rule
        try:
            candidates.update(driver.find_elements_by_xpath(rule))
        except:
            pass
    candidates = drop_non_digit_elements(candidates)  # is a list now
    if len(candidates) == 0:  # rule match failed
        return None, None

    mat = get_all_text_features(driver, candidates, img_ele)
    return candidates, mat


def get_all_text_features(driver, candidates, img_ele):
    """ Call get_text_features on each candidate and form np.array """
    win_size = driver.get_window_size()
    size_pct = [get_text_features(ele, win_size, img_ele) for ele in candidates]
    mat = np.array(size_pct)
    return mat


def labeling_hint(texts):
    """ Print elements text with index """
    for i, t in enumerate(texts):
        print(i, t)


def match_image_url(driver, url, partial=True):
    """
    Match image with @src=url on page opened in web driver
    :param driver: selenium.webdriver, with opened web page
    :param url: str, url of image (Usually stripped protocal and query part)
    :param partial: bool, partially match (contains) url (get rid of http and domain)
    :return: None or image node
    """
    # XPath match
    images = driver.find_elements_by_xpath('//img[contains(@src, "%s")]' % url)
    if len(images) == 0:
        half = url[:len(url) // 2]
        images = driver.find_elements_by_xpath('//img[contains(@src, "%s")]' % half)
        if len(images) == 0:
            return None
    if len(images) == 1:
        return images[0]
    else:
        # choose largest image
        def get_size(img):
            return int(img.get_attribute('width')), int(img.get_attribute('height'))

        size_list = list(map(get_size, images))
        a = np.array(size_list)
        choice = np.argmax(a[:, 0] * a[:, 1])
        return images[choice]


def get_text_features(ele, win_size, img_ele):
    """
    calculate element font size and position percentage in the window
    :param ele: selenium.webdriver.remote.webelement.WebElement
    :param win_size: {'height':, 'width':}
    :return: font_size, position_x, position_y by percentage,
    """

    try:
        x, y = ele.location['x'], ele.location['y']  # TODO: use location_once_scrolled?
    except:
        x, y = -1, -1
    win_h, win_w = win_size['height'], win_size['width']

    try:
        font_str = ele.value_of_css_property('font-size')
    except:
        font_str = -1
    # print(font_str)
    # print(type(font_str))
    font_size = int(config.REGEX_CACHE['num'].findall(font_str)[0])

    # calculate color contrast
    text_c = Color.from_string(ele.value_of_css_property('color'))
    back_c = Color.from_string(ele.value_of_css_property('background-color'))
    contrast = calc_color_contrast(rgb_unpack(text_c), rgb_unpack(back_c), float(text_c.alpha))

    # calculate luminance
    r, g, b = rgb_unpack(text_c)
    luminance = calc_luminance((r, g, b))

    # calculate img distance
    if img_ele is None:
        dx, dy, dxy = -1, -1, -1
    else:
        try:
            dx, dy, dxy = elements_dist(ele, img_ele)
        except StaleElementReferenceException:
            dx, dy, dxy = -1, -1, -1

    return font_size, float(x) / win_w, float(y) / win_h, contrast, luminance, dx, dy, dxy, r, g, b


def elements_dist(e1, e2):
    """
    :param e1: selenium.webdriver.remote.webelement.WebElement
    :param e2: same as above
    :return: abstract_distance_x, _y, quadratic distance
    """
    d1 = np.array((e1.location['x'], e1.location['y']))
    d2 = np.array((e2.location['x'], e2.location['y']))
    dist = np.abs(d1 - d2)
    return dist[0], dist[1], np.linalg.norm(dist)


def drop_non_digit_elements(elements):
    """
    Drop elements that does not include *digits*
    :param elements: [selenium.webdriver.remote.webelement.WebElement]
    :return: filtered list
    """
    return list(filter(lambda e: any(map(str.isdigit, e.text)), elements))


if __name__ == '__main__':
    logging.basicConfig(filename='tmp/scratch.py.log')
    # _test()
    # _multi_test()
    # _image_test()
