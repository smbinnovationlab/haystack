# -*- coding:utf-8 -*-

from conf import config
from PIL import Image
from selenium import webdriver
import logging


LOGGER = logging.getLogger(__name__)


def snip_website(url, path):
    """
    get website screenshot
    :param url: url
    :param path: path to save screenshot
    """

    # for Windows, set executable_path to the path of phantomjs.exe
    # executable_path = config.PHANTOMJS_EXEC_PATH
    # driver = webdriver.PhantomJS(executable_path=executable_path)
    # for Linux, install phantomjs and it does not require executable_path
    driver = webdriver.PhantomJS()

    driver.set_page_load_timeout(300)
    driver.set_window_size(1366, 768)
    try:
        driver.get(url)
        driver.save_screenshot(path)
        driver.quit()
        # crop
        im = Image.open(path)
        im = im.crop((0, 0, 1366, 1366))
        # resize
        im = im.resize((400, 400), Image.ANTIALIAS)
        im.save(path)
    except Exception as e:
        LOGGER.warning(str(e))
