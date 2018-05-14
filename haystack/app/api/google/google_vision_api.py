# -*- coding:utf-8 -*-

import os
import sys
sys.path.append('..' + os.path.sep + '..')

from conf import config
from db.db_operations import add_site, add_image_url, get_product_id, update_product_status
from urllib import request
import base64
import json
import os


def get_request_data(image_path, request_type, max_results):
    """
    upload an image and get related web entities by google vision api
    :param image_path: image file path
    :param max_results: max number of results returned
    :return: list of URLs
    """
    with open(image_path, 'rb') as img:
        image_content = base64.b64encode(img.read())
        image_content = image_content.decode(encoding='utf-8')

    requests = []
    a_request = {
        'image': {
            'content': image_content
        },
        'features': [
            {
                'type': request_type,
                'maxResults': max_results
            }
        ]
    }
    requests.append(a_request)
    requests = {
        'requests': requests
    }
    return json.dumps(requests).encode(encoding='utf-8')


def send_request(image_path, request_type, max_results):
    header_dict = {
        'Content-Type': 'application/json'
    }
    data = get_request_data(image_path, request_type, max_results)
    url = 'https://vision.googleapis.com/v1/images:annotate?key=' + get_api_key(config.GOOGLE_API_KEY_FILE)

    req = request.Request(url=url, data=data, headers=header_dict)
    res = request.urlopen(req)
    res = res.read().decode(encoding='utf-8')
    res_dict = eval(res)
    return res_dict


def get_web_urls(image_path, max_results):
    """
    get web URLs and update in DB
    :return: list of URLs
    """
    request_type = 'WEB_DETECTION'
    responses = send_request(image_path, request_type, max_results)
    responses = responses.get('responses')
    responses = responses[0]
    web_detection = responses.get('webDetection')
    full_match_images = web_detection.get('fullMatchingImages')
    web_pages = web_detection.get('pagesWithMatchingImages')
    images_urls = []
    urls = []
    if web_pages:
        for page in web_pages:
            url = page.get('url')
            urls.append(url)
    return urls


def get_web_urls_and_images(image_path, max_urls, max_image_urls=100):
    """
    get web URLs and update in DB
    :return: list of URLs
    """
    request_type = 'WEB_DETECTION'
    responses = send_request(image_path, request_type, max_urls)
    responses = responses.get('responses')
    responses = responses[0]
    web_detection = responses.get('webDetection')
    web_pages = None
    if web_detection:
        web_pages = web_detection.get('pagesWithMatchingImages')
    responses = send_request(image_path, request_type, max_image_urls)
    responses = responses.get('responses')
    responses = responses[0]
    web_detection = responses.get('webDetection')
    full_match_images = None
    partial_match_images = None
    if web_detection:
        full_match_images = web_detection.get('fullMatchingImages')
        partial_match_images = web_detection.get('partialMatchingImages')
    image_urls = []
    if full_match_images:
        for image in full_match_images:
            image_urls.append(image.get('url'))
    if partial_match_images:
        for image in partial_match_images:
            image_urls.append(image.get('url'))
    urls = []
    if web_pages:
        for page in web_pages:
            urls.append(page.get('url'))
    return image_urls, urls


def handle_images(image_path, max_results=100):
    if os.path.isdir(image_path):
        for rt, dirs, files in os.walk(image_path):
            for f in files:
                image_urls, urls = get_web_urls_and_images(os.path.join(image_path, f), max_results)
                sku_id = f.split('.')[0].split('_')[0]
                product_id = get_product_id(sku_id)
                if not product_id:
                    continue
                for url in urls:
                    add_site(url, product_id)
                for image_url in image_urls:
                    add_image_url(image_url, product_id)
    else:
        image_urls, urls = get_web_urls_and_images(image_path, max_results)
        sku_id = os.path.basename(image_path).split('_')[0]
        product_id = get_product_id(sku_id)
        if not product_id:
            return
        for url in urls:
            add_site(url, product_id)
        for image_url in image_urls:
            add_image_url(image_url, product_id)


def get_api_key(path):
    with open(path, 'r') as f:
        key = f.read()
    return key
