from django.conf.urls import url

from . import views


urlpatterns = [
    url('^upload__/$', views.upload__, name='lbattachment_upload__'),
    url('^delete__/$', views.delete__, name='lbattachment_delete__'),
    url('^change_descn__/$', views.change_descn__, name='lbattachment_change_descn__'),
    url('^download/$', views.download, name='lbattachment_download'),
]
