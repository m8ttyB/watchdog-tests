import io
from aiohttp import FormData, MultipartWriter
import urllib
import os
from mohawk import Sender
import molotov


path = '/accept'
negative_uri = 'https://watchdogproxy-default.dev.mozaws.net/mock/client/negative'
positive_uri = 'https://watchdogproxy-default.dev.mozaws.net/mock/client/positive'
positive_email = 'mbrandt@mozilla.com'

# stage config
if 'HAWK_KEY' not in os.environ:
    raise Exception('You need to set the HAWK_KEY environ')
url = 'https://watchdogproxy-default.stage.mozaws.net'
hawk_config = {'id': 'demouser',
               'key': os.environ.get('HAWK_KEY'),
               'algorithm': 'sha256'}
# dev config
# url = 'https://watchdogproxy-default.dev.mozaws.net'
# hawk_config = {'id': 'devuser',
#                'key': 'devkey',
#                'algorithm': 'sha256'}


async def get_content(writer):
    class Streamer:
        stream = io.BytesIO()
        async def write(self, data):
            self.stream.write(data)

    await writer.write(Streamer())
    Streamer.stream.seek(0)

    return Streamer.stream.read()


def get_form():
    form = FormData()
    form.add_field("negative_uri", negative_uri)
    form.add_field("positive_uri", positive_uri)
    form.add_field("positive_email", positive_email)
    return form

@molotov.scenario(weight=50)
async def test_negative_large_img(session):
    headers = {'Authorization': ''}
    with MultipartWriter(subtype='form-data') as writer:
        writer.append_form({'boaty': 'mc boat face'})
        raw = await get_content(writer)
        sender = Sender(hawk_config, url + path, 'POST',
                        content=raw,
                        content_type='multipart/form-data')
        headers['Authorization'] = sender.request_header
    form = get_form()
    form.add_field("image", open('images/img_positive.jpg', 'rb').read(),
                   filename="images/img_4.3.jpg")
    async with session.post(url + path, data=form, headers=headers) as resp:
        assert resp.status == 201, \
            'Status code: %s URL: %s Headers: %s Content: %s' % \
            (resp.status, resp.url, resp.headers, resp.content)


@molotov.scenario(weight=50)
async def test_positive(session):
    headers = {'Authorization': ''}
    with MultipartWriter(subtype='form-data') as writer:
        writer.append_form({'boaty': 'mc boat face'})
        raw = await get_content(writer)
        sender = Sender(hawk_config, url + path, 'POST',
                        content=raw,
                        content_type='multipart/form-data')
        headers['Authorization'] = sender.request_header
    form = get_form()
    form.add_field("image", open('images/img_positive.jpg', 'rb').read(),
                   filename="images/img_positive.jpg")
    async with session.post(url + path, data=form, headers=headers) as resp:
        json = await resp.json()
        assert 'id' in json
        assert 'negative_uri' in json
        assert 'positive_uri' in json
        assert 'positive_email' in json
        assert resp.status == 201, \
            'Status code: %s URL: %s Headers: %s Content: %s' % \
            (resp.status, resp.url, resp.headers, resp.content)
