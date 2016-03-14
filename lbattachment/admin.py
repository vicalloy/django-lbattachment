# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import LBAttachment


class LBAttachmentAdmin(admin.ModelAdmin):
    search_fields = ('user__username', 'filename', 'act_members_param', 'notice_members_param', 'share_members_param')
    list_display = ('user', 'filename', 'is_img', 'num_downloads', 'is_active', )
    list_filter = ('is_img', 'suffix')
    raw_id_fields = ('user',)

admin.site.register(LBAttachment, LBAttachmentAdmin)
