# -*- coding:utf-8 -*-

import os
import sys
sys.path.append('..' + os.path.sep)

# file directory
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__) + os.path.sep + '..' + os.path.sep + '..')
PRODUCT_IMAGE_DIR = os.path.join(PROJECT_DIR, ''.join([d + os.path.sep for d in ['data', 'pic', 'product']]))
PRODUCT_IMAGE_DIR_1 = os.path.join(PROJECT_DIR, ''.join([d + os.path.sep for d in ['data', 'pic', 'product_1']]))
RULE_DIR = os.path.join(PROJECT_DIR, ''.join([d + os.path.sep for d in ['app', 'rules']]))
URL_CRAWLED_DATA_DIR = os.path.join(PROJECT_DIR, ''.join([d + os.path.sep for d in ['data', 'raw']]))
PRODUCT_MAIN_IMAGE_DIR = os.path.join(PROJECT_DIR, ''.join([d + os.path.sep for d in ['data', 'pic', 'product_main']]))
SITE_SCREENSHOT_DIR = os.path.join(PROJECT_DIR, ''.join([d + os.path.sep for d in ['data', 'pic', 'screenshot']]))

# admin server url
# ADMIN_SERVER_URL = 'http://127.0.0.1:5001/'             # for local
ADMIN_SERVER_URL = 'http://server_admin:5001/'        # for docker

# GOOGLE_CLOUD_API_KEY = ''
GOOGLE_API_KEY_FILE = os.path.join(PROJECT_DIR,
                                   os.path.sep.join(['app', 'conf', 'google_api_key.txt']))

# phantomjs executable path
PHANTOMJS_EXEC_PATH = ''
