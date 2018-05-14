import itertools
import logging
from difflib import get_close_matches, SequenceMatcher
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException

from . import config
from .utils import timeit_dec


@timeit_dec
def dom_search(driver, bs=None):
    """
    Search in html for pattern (price). Need either argument
    :param driver: selenium.webdriver
    :param bs: BeautifulSoup
    :return: [selenium node element], [str]
    """
    if bs is None:
        html = driver.execute_script("return document.body.innerHTML;")
        bs = BeautifulSoup(html, 'html5lib')
    body = bs.find(name='body')
    candidates = cascade_regex_find(body)

    elements = []
    texts = []
    for c in candidates:
        # selector = get_css_path(c.parent)
        # print(selector)
        selector = xpath_soup(c.parent)
        try:
            ele = driver.find_element_by_xpath(selector)
            # ele = driver.find_element_by_css_selector(selector)
        except NoSuchElementException as e:
            logging.warning('Element not found with selector ' + selector)
            continue

        # filter by currency sign
        if any(config.REGEX_CACHE['currency'].findall(c)):
            t = str(c).strip()
        else:
            t = str(c.parent.text).strip()
        if len(t) == 0:
            continue

        # filter by deletion line
        try:
            if ele.value_of_css_property('text-decoration').index('line-through') >= 0:
                continue
        except:
            pass

        elements.append(ele)
        texts.append(t)

    if len(elements) > 5:
        try:
            mask = [e.is_displayed() for e in elements]
            elements = [e for e, m in zip(elements, mask) if m]
            texts = [t for t, m in zip(texts, mask) if m]
        except Exception:
            logging.warning('Element visibility check failed')
            pass

    return elements, texts


def cascade_regex_find(body):
    """ Use multiple regex to find price-format text in html.body """
    names = ['money', 'money_pre', 'money_suf', 'money_comma']
    candidates = []

    def _filter(c):
        # has text, text part not too long, not deleted
        return list(filter(
            lambda x: len(x.strip()) > 0 and len(x.parent.text.strip()) <= 40 and x.parent.name != 'del',
            c
        ))

    for n in names:
        temp = _filter(body.find_all(text=config.REGEX_CACHE[n]))
        logging.info('%d candidates by REGEX %s' % (len(temp), n))
        candidates.extend(temp)
        if len(candidates) > 12:        # TODO: check thresh
            break

    if len(candidates) < 4:             # look in parent node for money_pre
        temp = _filter(body.find_all(text=config.REGEX_CACHE['num']))
        pre_reg = config.REGEX_CACHE['money_pre']
        new_candidates = []
        for n in temp:
            text = n.parent.parent.text
            if any(pre_reg.finditer(text)):
                new_candidates.append(n)
        new_candidates = _filter(new_candidates)
        logging.info('%d candidates by parent search' % len(new_candidates))
        candidates.extend(new_candidates)
    return candidates


@timeit_dec
def get_image_match(driver, possibilities, bs=None):
    """
    Get image elements match (same or close)
    :param driver: selenium.webdriver
    :param possibilities: [str], image url possibilities for matching
    :param bs: BeautifulSoup, build from driver.page_source if None
    :return: selenium.WebElement, image node
    """
    if bs is None:
        html = driver.execute_script("return document.body.innerHTML;")
        bs = BeautifulSoup(html, 'html5lib')
    images = bs.find_all(name='img', src=True)      # guaranteed to have 'src'
    page_urls = [im['src'] for im in images]
    matches = set(possibilities).intersection(page_urls)

    tag = None                                      # matched bs element
    if len(matches) == 0:                           # similarity match
        max_ratio = 0
        for i, u in enumerate(page_urls):
            temp = get_close_matches(u, possibilities, 1)
            if len(temp) == 0:
                continue
            temp = temp[0]
            r = SequenceMatcher(None, temp, u).ratio()
            if r > max_ratio:
                max_ratio = r
                tag = images[i]
        if tag is None:
            return None
        logging.info('Partial match image url by %g' % max_ratio)
    else:
        match = list(matches)[0]
        tag = bs.find(name='img', src=match)
        logging.info('Exact url-match image')

    path = get_css_path(tag)
    # print(path)
    try:
        ele = driver.find_element_by_css_selector(path)     # convert to selenium element
        if config.INTERACTIVE:
            driver.execute_script(                              # insert hint
                'arguments[0].parentElement.innerHTML += "<p>MagicHS</p>" + arguments[0].parentElement.innerHTML',
                ele
            )
    except Exception as e:
        logging.warning('css selector fail ' + path)
        ele = None
    return ele


def get_element(node):
    """
    credit to Dmytro Sadovnychyi @ stackoverflow
    https://stackoverflow.com/questions/25969474/beautifulsoup-extract-xpath-or-css-path-of-node
    :param node:
    :return:
    """
    try:                            # try use id
        id = node['id']
        if len(id) > 0:
            return '#' + str(id)
    except:
        pass

    length = len(list(node.find_previous_siblings())) + 1   # TODO: check whether this avoid non-element node
    if length > 1:
        return '%s:nth-child(%s)' % (node.name, length)
    else:
        return node.name


def get_css_path(node):
    """
    credit to Dmytro Sadovnychyi @ stackoverflow
    https://stackoverflow.com/questions/25969474/beautifulsoup-extract-xpath-or-css-path-of-node
    :param node:
    :return:
    """
    path = [get_element(node)]
    for parent in node.parents:
        if parent.name == 'html':
            break
        desc = get_element(parent)
        path.insert(0, desc)
        if desc.startswith('#'):        # unique id found
            break
    return '>'.join(path)


def shorten_image_urls(urls):
    """
    Extract domain and path, get rid of protocol, domain and query
    :param urls: str
    :return: str, shorten
    """
    def extract(u):
        o = urlparse(u)
        return o.path
    return list(map(extract, urls))


def xpath_soup(element):
    """
    Generate xpath of soup element
    credit to ergoithz @GitHub
    :param element: bs4 text or node
    :return: xpath as string
    """
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:
        """
        @type parent: bs4.element.Tag
        """
        previous = itertools.islice(parent.children, 0, parent.contents.index(child))
        try:
            id = child['id']
            if len(id) > 0:
                components.append('/*[@id="%s"]' % id)      # //*[@id=""], the other slash is added at return
                break
        except:
            pass
        xpath_tag = child.name

        xpath_index = sum(1 for i in previous if i.name == xpath_tag) + 1
        components.append('%s[%d]' % (xpath_tag, xpath_index))
        child = parent
    components.reverse()
    return '/' + '/'.join(components)


def _test():
    from selenium import webdriver
    d = webdriver.Chrome()
    d.get('http://www.morrans-international.com/product_info.php/022000158925-altoids-peppermint-50g-p-6777')
    e, t = dom_search(d)
    print(t)


if __name__ == '__main__':
    _test()

