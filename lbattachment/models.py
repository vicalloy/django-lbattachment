import datetime
import os

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from . import settings as lb_settings
from django.utils.encoding import python_2_unicode_compatible

from lbutils import format_filesize


try:
    AUTH_USER_MODEL = settings.AUTH_USER_MODEL
except:
    AUTH_USER_MODEL = User


def is_img(suffix):
    suffix = suffix.lower()
    return lb_settings.LBATTACHMENT_IMG_SUFFIX_LIST.count(suffix) > 0


def upload_attachment_file_path(instance, filename):
    instance.filename = os.path.basename(filename)
    path = "works/%s/%s/%s/%s" % (
        instance.created_by.pk,
        datetime.datetime.now().strftime('%Y%m%d'),
        instance.filename)
    return os.path.join(lb_settings.LBATTACHMENT_STORAGE_DIR, path)


@python_2_unicode_compatible
class LBAttachment(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, verbose_name=_('Attachment'))
    attach_file = models.FileField(max_length=255, upload_to=upload_attachment_file_path)
    filename = models.CharField(max_length=255)
    suffix = models.CharField(default='', max_length=8, blank=True)
    is_img = models.BooleanField(default=False)
    num_downloads = models.IntegerField(default=0)
    description = models.TextField(default='', blank=True)
    is_active = models.BooleanField(default=False)

    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User)

    def __str__(self):
        return '%s|%s' % (self.user.username, self.filename)

    def get_formated_filesize(self):
        return format_filesize(self.file.size)
