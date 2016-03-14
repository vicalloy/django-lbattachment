# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

import tempfile
import json
from django.test import TestCase
from django.core.urlresolvers import reverse


class BaseCase(TestCase):

    fixtures = ['test_lbattachment.json']

    def assertRespSucc(self, resp):
        d = json.loads(resp.content)
        self.assertTrue(d['valid'])

    def assertRespFail(self, resp):
        d = json.loads(resp.content)
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
        tmp_file = tempfile.NamedTemporaryFile(suffix='.txt')
        tmp_file.write("Hello World!\n")
        tmp_file.close()
        p['attach_file'] = tmp_file
        resp = self.client.post(reverse('lbattachment_upload__'), p, format='multipart')
        self.assertRespSucc(resp)

    def test_download(self):
        p = {'pk': 1}
        resp = self.client.get(reverse('lbattachment_download'), p)
        self.assertRespFail(resp)
        self.login('u1')
        resp = self.client.get(reverse('lbattachment_download'), p)
        self.assertRespFail(resp)
