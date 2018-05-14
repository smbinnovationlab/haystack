# -*- coding:utf-8 -*-

import os
import sys
sys.path.append('..' + os.path.sep)


PROJECT_DIR = os.path.abspath(os.path.dirname(__file__) + os.path.sep + '..' + os.path.sep + '..')
PRODUCT_UPLOAD_DIR = os.path.join(PROJECT_DIR, ''.join([d + os.path.sep for d in ['data', 'pic', 'product_upload']]))
GOOGLE_VISION_DIR = os.path.join(PROJECT_DIR, ''.join([d + os.path.sep for d in ['data', 'pic', 'google_vision']]))
RULE_DIR = os.path.join(PROJECT_DIR, ''.join([d + os.path.sep for d in ['app', 'rules']]))
URL_CRAWLED_DATA_DIR = os.path.join(PROJECT_DIR, ''.join([d + os.path.sep for d in ['data', 'raw']]))
PRODUCT_MAIN_IMAGE_DIR = os.path.join(PROJECT_DIR, ''.join([d + os.path.sep for d in ['data', 'pic', 'product_main']]))
SITE_SCREENSHOT_DIR = os.path.join(PROJECT_DIR, ''.join([d + os.path.sep for d in ['data', 'pic', 'screenshot']]))

LOG_FILE_DIR = os.path.join(PROJECT_DIR, ''.join([d + os.path.sep for d in ['app', 'tmp']]))
LOG_FILE_NAME = 'analyzer.log'

# for local
# ADMIN_SERVER_URL = 'http://127.0.0.1:5002/'
# for docker
ADMIN_SERVER_URL = 'http://server_admin:5002/'

MQ_CONNECTION_HOST = 'mq'
MQ_TASK_QUEUE = 'haystack_task_queue'
MQ_QUEUE_1ST = 'microdata_queue'
MQ_QUEUE_2ND = 'url_pattern_queue'
MQ_QUEUE_3RD = 'multi_analyzer_queue'
WEB_SERVER_URL = 'http://web_server:5004'

# GOOGLE_CLOUD_API_KEY = ''
GOOGLE_API_KEY_FILE = os.path.join(PROJECT_DIR,
                                   os.path.sep.join(['app', 'conf', 'google_api_key.txt']))

# phantomjs executable path for Windows
PHANTOMJS_EXEC_PATH = ''
