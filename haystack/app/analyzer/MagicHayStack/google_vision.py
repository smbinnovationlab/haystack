from google.cloud import vision
from google.cloud.vision import types


def query_web_detection(img_url, max_results=20):
    client = vision.ImageAnnotatorClient()
    d = {
            'image': {
                'source': {
                    'image_uri': img_url
                }
            },
            'features': [{
                'type': 'WEB_DETECTION',
                'max_results': max_results
            }]
        }
    response = client.annotate_image(d).web_detection
    return response


def unpack_json(j):
    j = j['webDetection']
    for p in j['pagesWithMatchingImages']:
        print(p['url'])
    print('\n\n')

    for p in j['partialMatchingImages']:
        print(p['url'])


def _test():
    """
    Change the url below, get all full_matching_images and pages_with_matching_images in the console
    :return:
    """
    r = query_web_detection("https://images-cn.ssl-images-amazon.com/images/I/61rxMvX9BKL._SY679_.jpg", 5000)
    for url in r.partial_matching_images:
        print(url.url)
    print('\n')
    for url in r.pages_with_matching_images:
        print(url.url)


if __name__ == '__main__':
    _test()