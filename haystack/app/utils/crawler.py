# -*- coding:utf-8 -*-

import os
import sys
sys.path.append('..' + os.path.sep)

from conf import config
from db.db_operations import check_site_by_id
from db.mysql_conf import mysql_engine
from db.object_definition import Site
from sqlalchemy.orm import sessionmaker
import datetime
import random
import time
import urllib.error
import urllib.request


def crawl_data(url, site_id, max_retry_times):
    """
    crawl and save url raw data in local
    :param url: url
    :param site_id: site_id as file name
    :param max_retry_times: max retry times
    :return: True if success, else False
    """
    success_flag = False
    if not check_site_by_id(site_id):
        return success_flag

    current_retry_count = 0
    while current_retry_count < max_retry_times:
        try:
            req_headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)'}
            req = urllib.request.Request(url, headers=req_headers)
            response = urllib.request.urlopen(req, timeout=60)
            content = response.read()
            # Save to file
            data_file_path = config.URL_CRAWLED_DATA_DIR + str(site_id) + '_new'
            with open(data_file_path, 'wb') as f:
                f.write(content)
            # update last indexed time in DB(haystack/site)
            engine = mysql_engine()
            db_session = sessionmaker(bind=engine)
            session = db_session()
            session.query(Site).filter(Site.site_id == site_id).update(
                {Site.last_indexed: datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
            session.commit()
            session.close()
            success_flag = True
            break
        except urllib.error.HTTPError as e:
            print(e.code, e.reason)
            current_retry_count += 1
            print('Retry:', current_retry_count, '/', max_retry_times)
            continue
        except urllib.error.URLError as e:
            print(e.reason)
            current_retry_count += 1
            print('Retry:', current_retry_count, '/', max_retry_times)
            continue
        except ConnectionResetError as e:
            print('ConnectionResetError')
            time.sleep(random.uniform(0, 2))
            current_retry_count += 1
            print('Retry:', current_retry_count, '/', max_retry_times)
            continue
        except Exception as e:
            print('Unexpected exception:', str(e))
            break
    return success_flag


def save_image(url, save_path):
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req, timeout=60)
    # content_type = response.info().get('Content-Type')
    # if 'image' not in content_type:
    #     return
    # image_type = content_type.split('/')[1]
    # save_path = save_path + '.' + image_type

    # Save to file
    content = response.read()
    with open(save_path, 'wb') as f:
        f.write(content)
