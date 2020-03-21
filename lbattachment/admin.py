from django.contrib import admin

from .models import LBAttachment


class LBAttachmentAdmin(admin.ModelAdmin):
    search_fields = ('created_by__username', 'filename', 'act_members_param', 'notice_members_param', 'share_members_param')
    list_display = ('created_by', 'filename', 'is_img', 'num_downloads', 'is_active', )
    list_filter = ('is_img', 'suffix')
    raw_id_fields = ('created_by',)


admin.site.register(LBAttachment, LBAttachmentAdmin)
