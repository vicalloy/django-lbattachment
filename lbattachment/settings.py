from django.conf import settings

LBATTACHMENT_X_ACCEL = getattr(settings, 'LBATTACHMENT_X_ACCEL', False)
LBATTACHMENT_STORAGE_DIR = getattr(settings, 'LBATTACHMENT_STORAGE_DIR', 'lbattachments')
LBATTACHMENT_MEDIA_URL = getattr(settings, 'LBATTACHMENT_MEDIA_URL', 'lbattachments')
LBATTACHMENT_IMG_SUFFIX_LIST = getattr(settings, 'LBATTACHMENT_IMG_SUFFIX_LIST', ['png', 'gif', 'jpg', 'jpeg'])
LBATTACHMENT_IMG_SUFFIX_LIST = [e.lower() for e in LBATTACHMENT_IMG_SUFFIX_LIST]
