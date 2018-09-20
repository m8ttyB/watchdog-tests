#!/usr/bin/env python
import os

import requests
from requests_hawk import HawkAuth


if 'HAWK_KEY' not in os.environ:
    raise Exception('You need to set the HAWK_KEY environ')

url = 'https://watchdogproxy-default.stage.mozaws.net'
path = '/accept'
webhook = 'https://webhook.site/dd8f6f51-270d-4d16-bcca-9a10c8f063b7'
negative_uri = webhook
positive_uri = webhook
positive_email = 'mbrandt@mozilla.com'

id = 'demouser'
key = os.environ.get('HAWK_KEY')

form_data = {
    'negative_uri': negative_uri,
    'positive_uri': positive_uri,
    'positive_email': positive_email,
}

def _get_bits(image):
    with open(image, 'rb') as f:
        return f.read()

def list_files():
    for path, subdirs, files in os.walk(r'images/sample_images'):
        return files


def file_data(image):
    image_data = _get_bits(image)
    return {'image': (image, image_data)}


def submit_image(file):
    auth = HawkAuth(id=id, key=key)
    return requests.post(url + path,
                         data=form_data, files=file_data(file),
                         auth=auth)


def test_positive_jpeg():
    resp = submit_image('images/img_positive.jpg')
    assert resp.status_code is 201, resp.status_code


def test_negative():
    resp = submit_image('images/img_negative.jpg')
    assert resp.status_code is 201, resp.status_code


def test_large():
    resp = submit_image('images/img_large.jpg')
    print(resp.headers)
    print(resp.content)
    assert resp.status_code is 201, resp.status_code


def test_positive_png_image():
    resp = submit_image('images/img_png_positive.png')
    assert resp.status_code is 201, resp.status_code


def test_fuzz():
    image_data = 'mattb' * 1000000
    file_data = {'image': ('mattb.jpg', image_data)}
    auth = HawkAuth(id=id, key=key)
    resp = requests.post(url + path,
                         data=form_data, files=file_data,
                         auth=auth)
    assert resp.status_code is 201, resp.status_code
