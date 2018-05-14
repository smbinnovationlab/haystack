import os

from selenium.common.exceptions import TimeoutException

from .dom_search import *
from .feature import *


def interactive_labeling(page_url_file, img_url_file):
    """ Reading page urls and image urls, wait user labeling to build training data """
    config.INTERACTIVE = True
    with open(page_url_file, 'r') as f:
        page_urls = f.readlines()
        page_urls = map(str.strip, page_urls)
        logging.info('Using page urls from %s' % page_url_file)
    with open(img_url_file, 'r') as f:
        image_urls = f.readlines()
        image_urls = map(str.strip, image_urls)
        logging.info('Using image urls from %s' % img_url_file)
    image_urls = set(shorten_image_urls(image_urls))        # get rid of domain and query part

    driver = config.GET_WEB_DRIVER()
    driver.implicitly_wait(60)
    # driver.set_page_load_timeout(60)
    for u in page_urls:
        # Access url
        candidates, texts, mat, _ = access_url(driver, u, image_urls)
        if candidates is None:
            continue

        # user labeling
        labeling_hint(texts)
        for i, c in enumerate(candidates):          # inject visual hint to web page
            try:
                driver.execute_script('arguments[0].innerHTML += "[%s]"' % (str(i)), c)
            except:
                pass
        choice = parse_input(input('\nWhich is the real price?'))
        if len(choice) == 1 and choice[0] == -1:
            logging.info('Not recording this one')
            continue
        win_size = driver.get_window_size()
        h, w = win_size['height'], win_size['width']

        # write results
        if not os.path.exists(config.DATA_SAVE_FILE):
            with open(config.DATA_SAVE_FILE, 'a', encoding='utf-8') as f:
                f.write('url,font_size,x_pct,y_pct,contrast,luminance,dx,dy,dxy,r,g,b,currency,win_x,win_y,class,text')

        with open(config.DATA_SAVE_FILE, 'a', encoding='utf-8') as f:
            for i, row in enumerate(mat):
                f.write(u + ',')
                for data in row:
                    f.write(str(data) + ',')
                f.write(str(h) + ',')
                f.write(str(w) + ',')

                if i in choice:
                    f.write('1,')
                else:
                    f.write('0,')
                f.write(sanitize_text(texts[i]) + '\n')
        logging.info('Saved\n')
    driver.close()


def access_url(driver, url, image_urls):
    """
    return all features and information found in url
    :param driver:
    :param url:
    :param image_urls:
    :return: candidates, texts, mat, is_image_found
    """
    try:
        driver.get(url)
    except TimeoutException:
        logging.warning('Page load time out')
        # if driver.current_url != url:
        #     logging.warning('Browser restart for failing to navigate to new url')
        #     return None, None, None
    logging.info('Access url %s' % url)
    bs = BeautifulSoup(driver.page_source, 'html5lib')

    # match image
    image_urls = shorten_image_urls(image_urls)
    img_ele = get_image_match(driver=driver, possibilities=image_urls, bs=bs)
    if img_ele is None:
        logging.warning('Image not found')

    # extract features
    # candidates, mat = find_price_by_rule(driver, config.XPATH_RULE_SAMPLES, img_ele)
    candidates = None
    if candidates is None or len(candidates) == 0:
        # logging.warning('No price tag found in url %s' % url)

        # try text based search
        candidates, texts = dom_search(driver=driver, bs=bs)
        if len(candidates) == 0:  # still failed
            logging.warning('No price text found in url %s' % url)
            return None, None, None, None
        mat = get_all_text_features(driver, candidates, img_ele)
    else:
        texts = [c.text for c in candidates]  # extract texts from elements

    currency_sign = np.array(list(map(lambda x: any(config.REGEX_CACHE['currency'].finditer(x)), texts)), dtype=np.int)
    currency_sign = currency_sign.reshape((-1, 1))
    mat = np.concatenate((mat, currency_sign), 1)

    logging.info('Find %d candidates' % len(mat))
    return candidates, texts, mat, (img_ele is not None)


def find_largest_image(images):
    """
    Return image with largest area
    :param images:
    :return:
    """
    def get_size(img):
        return int(img.get_attribute('width')) * int(img.get_attribute('height'))

    size_list = list(map(get_size, images))
    choice = np.array(size_list).argmax()
    return images[choice]


def sanitize_text(s):
    """ get rid of '\n,' that sabotage CSV file """
    return s.replace('\n', '').replace(',', '')


def find_all_image_urls(driver):
    """ Find urls of all image opened on a web page (Shortened) """
    images = []
    try:
        images = driver.find_elements_by_xpath('//img')
    except TimeoutException:
        logging.warning('Find all image timeout')
        pass
    urls = [None] * len(images)
    for i, im in enumerate(images):
        try:
            urls[i] = im.get_attribute('src')
        except Exception:
            logging.warning('Get image src timeout/stale (No.%d)' % i)
            urls[i] = ''
    urls = shorten_image_urls(urls)
    return images, urls


def parse_input(s):
    """
    Parse labeling input, int separated by comma
    :param s: \d(,\d)*
    :return: [int]
    """
    l = s.split(',')
    try:
        ret = list(map(int, l))
    except ValueError:
        return []
    return ret


def _test():
    interactive_labeling(config.PAGE_URLS_FILE, config.IMG_URLS_FILE)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)-10s 	%(levelname)-8s %(message)s", datefmt='%H:%M:%S')
    _test()
