#!/usr/bin/env python
import os

#import pytest
import requests
from requests_hawk import HawkAuth

# url = 'https://watchdogproxy-default.stage.mozaws.net'
url = 'https://watchdogproxy-default.stage.mozaws.net'
path = '/accept'
webhook = 'https://webhook.site/20492752-5b4a-47fd-a440-614d22860fb1'
# negative_uri = 'https://watchdog-proxy.dev.mozaws.net/mock/client/negative'
# negative_uri = 'https://watchdogproxy-default.stage.mozaws.net/mock/client/negative'
# positive_uri = 'https://watchdog-proxy.dev.mozaws.net/mock/client/positive'
# positive_uri = 'https://watchdogproxy-default.stage.mozaws.net/mock/client/positive'
negative_uri = webhook
positive_uri = webhook
positive_email = 'mbrandt@mozilla.com'

id = 'demouser'
key = '<key>'

form_data = {
    'negative_uri': negative_uri,
    'positive_uri': positive_uri,
    'positive_email': positive_email,
}

def get_bits(image):
    with open(image, 'rb') as f:
        return f.read()

def list_files():
    for path, subdirs, files in os.walk(r'images/sample_images'):
        return files


def file_data(image):
    image_data = get_bits(image)
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
    image_data = 'mattb' * 100000
    file_data = {'image': ('mattb.jpg', image_data)}
    auth = HawkAuth(id=id, key=key)
    resp = requests.post(url + path,
                         data=form_data, files=file_data,
                         auth=auth)
    assert resp.status_code is 21, resp.status_code
