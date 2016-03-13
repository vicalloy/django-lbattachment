from django.conf import settings
LBATTACHMENT_STORAGE_DIR = getattr(settings, 'LBATTACHMENT_STORAGE_DIR', 'lbattachments')
