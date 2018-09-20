#!/usr/bin/env python
import os

import requests
from requests_hawk import HawkAuth


path = '/accept'
webhook = 'https://webhook.site/229e69b2-4bbf-4d47-be56-1a341e7e5bae'
negative_uri = webhook
positive_uri = webhook
positive_email = 'mbrandt@mozilla.com'

# stage vars
if 'HAWK_KEY' not in os.environ:
    raise Exception('You need to set the HAWK_KEY environ')
url = 'https://watchdogproxy-default.stage.mozaws.net'
id = 'demouser'
key = os.environ.get('HAWK_KEY')

# dev vars
# url = 'https://watchdogproxy-default.dev.mozaws.net'
# id = 'devuser'
# key = 'devkey'

form_data = {
    'negative_uri': negative_uri,
    'positive_uri': positive_uri,
    'positive_email': positive_email,
}

def _get_bits(image):
    with open(image, 'rb') as f:
        return f.read()

def _list_files(dir):
    for path, subdirs, files in os.walk(dir):
        return files


def _file_data(filename):
    image_data = _get_bits(filename)
    return {'image': (filename, image_data)}


def submit_image(file):
    auth = HawkAuth(id=id, key=key)
    return requests.post(url + path,
                         data=form_data, files=_file_data(file),
                         auth=auth)

def inspect_request():
    auth = HawkAuth(id=id, key=key)
    req = requests.Request('POST', url, data=form_data, files=_file_data('images/img_positive.jpg'), auth=auth)
    prepared = req.prepare()
    print(prepared.body[:800])


def test_sumbit_sample_images():
    dir = 'images/sample_images/'
    files = _list_files(dir)
    for file in files:
        submit_image(dir + file)


if __name__ == '__main__':
    inspect_request()
