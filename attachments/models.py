from time import time
from random import randint
import os

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


try:
    AUTH_USER_MODEL = settings.AUTH_USER_MODEL
except:
    AUTH_USER_MODEL = User


def format_filesize(size_in_bytes):
    SIZE_KEYS = ['B', 'KB', 'MB']
    try:
        size_in_bytes = int(size_in_bytes)
    except ValueError:
        return size_in_bytes
    if size_in_bytes<1:
        return '%d %s'% (0,SIZE_KEYS[2])
    size_in_bytes, divider = int(size_in_bytes), 1 << 20
    major = size_in_bytes / divider
    while not major:
        major = size_in_bytes / divider
        if not major:
            divider >>= 10
    rest = size_in_bytes - major * divider
    scale = 10
    fract = int(float(rest) / divider * scale)
    cnt = 0
    while divider:
        cnt += 1
        divider >>= 10
    value = major + fract * (1.0 / scale)
    ivalue = int(value)
    if value == ivalue:
        value = ivalue
    return '%d %s'% (value,SIZE_KEYS[cnt - 1])

def get_file_suffix(filename):
    idx = filename.rfind('.')
    return filename[idx+1:]

def is_img(suffix):
    suffix = suffix.lower()
    img_suffix = ['png', 'gif', 'jpg', 'jpeg']
    return img_suffix.count(suffix) > 0

def upload_attachment_file_path(instance, filename):
    instance.org_filename = get_filename(filename)
    suffix = get_file_suffix(filename)
    instance.suffix = suffix
    instance.is_img = is_img(suffix)
    t = str(time()).replace('.', '_')
    r = randint(1, 1000)
    fn = '%s_%s.%s' % (t, r, suffix)
    return os.path.join(settings.ATTACHMENT_STORAGE_DIR, fn)

def get_filename(filename):
    """remove path"""
    def lt(f, x):
        f=f.split(x)
        f=f[len(f)-1]
        return f
    return lt(lt(filename, '\\'), '/')

class Attachment(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, verbose_name=_('Attachment'))
    file = models.FileField(max_length=255, upload_to=upload_attachment_file_path)
    org_filename = models.TextField()
    suffix = models.CharField(default = '', max_length=8, blank=True)
    is_img = models.BooleanField(default=False)
    num_downloads = models.IntegerField(default=0)
    description = models.TextField(default = '', blank=True)
    activated = models.BooleanField(default=False)
    date_uploaded = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s|%s' % (self.user.username, self.file)
        
    def get_formated_filesize(self):
        return format_filesize(self.file.size)
