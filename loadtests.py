#!/usr/bin/env python
import requests
from requests_hawk import HawkAuth

import molotov

image = 'images/book.jpg'
url = 'https://watchdogproxy-default.stage.mozaws.net'
path = '/accept'

negative_uri = 'https://webhook.site/8550f8d5-6da3-41de-8609-f7d0690bd6ff'
positive_uri = 'https://webhook.site/8550f8d5-6da3-41de-8609-f7d0690bd6ff'
positive_email = 'mbrandt@mozilla.com'

id = 'demouser'
key = '<key>'


def get_bits(image):
    with open(image, 'rb') as f:
        return f.read()


form_data = {
    'negative_uri': negative_uri,
    'positive_uri': positive_uri,
    'positive_email': positive_email,
    'image': (get_bits(image), '12345' 'image/jpeg')
}


@molotov.scenario(weight=100)
async def test_simple(session):
    hawk_auth = HawkAuth(id=id, key=key)
    async with session.post(url + path,
                            data=form_data,
                            auth=hawk_auth) as resp:
        assert resp.status_code is 201, resp.status_code
