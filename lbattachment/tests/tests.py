import json

import django
from django.test import TestCase

from lbattachment import settings as lb_settings

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse


def resp_as_json(resp):
    if django.VERSION < (1, 9, 0):
        d = json.loads(resp.content.decode('utf8'))
    else:
        d = resp.json()
    return d


class BaseCase(TestCase):

    fixtures = ['test_lbattachment.json']

    def assertRespSucc(self, resp):
        d = resp_as_json(resp)
        self.assertTrue(d['valid'])

    def assertRespFail(self, resp):
        d = resp_as_json(resp)
        self.assertFalse(d['valid'])


class LBAttachmentTest(BaseCase):

    def login(self, username):
        self.client.login(username=username, password='138')

    def test_lbattachment_delete__(self):
        p = {'pk': 1}
        resp = self.client.get(reverse('lbattachment_delete__'), p)
        self.assertRespFail(resp)
        self.login('u1')
        resp = self.client.get(reverse('lbattachment_delete__'), p)
        self.assertRespFail(resp)
        self.login('u2')
        resp = self.client.get(reverse('lbattachment_delete__'), p)
        self.assertRespSucc(resp)

    def test_change_descn__(self):
        p = {'pk': 1}
        resp = self.client.post(reverse('lbattachment_change_descn__'), p)
        self.assertRespFail(resp)
        self.login('u1')
        resp = self.client.post(reverse('lbattachment_change_descn__'), p)
        self.assertRespFail(resp)
        self.login('u2')
        resp = self.client.post(reverse('lbattachment_change_descn__'), p)
        self.assertRespSucc(resp)

    def test_upload__(self):
        p = {}
        p['attach_file'] = open(__file__, "rb")
        resp = self.client.post(reverse('lbattachment_upload__'), p)
        p['attach_file'].close()
        self.assertRespFail(resp)
        self.login('u1')
        p['attach_file'] = open(__file__, "rb")
        resp = self.client.post(reverse('lbattachment_upload__'), p)
        p['attach_file'].close()
        self.assertRespSucc(resp)

    def test_download(self):
        lb_settings.LBATTACHMENT_X_ACCEL = True
        p = {'pk': 1}
        resp = self.client.get(reverse('lbattachment_download'), p)
        self.assertEqual(resp.status_code, 302)
        self.login('u1')
        resp = self.client.get(reverse('lbattachment_download'), p)
        self.assertEqual(resp.status_code, 200)
        lb_settings.LBATTACHMENT_X_ACCEL = False
        self.login('u1')
        resp = self.client.get(reverse('lbattachment_download'), p)
        self.assertTrue('attachments/2016/01/14/cp.png' in resp['location'])
