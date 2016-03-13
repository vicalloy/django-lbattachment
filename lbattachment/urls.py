from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url('^ajax_upload/$', views.ajax_upload, name='lbattachment_ajax_upload'),
    url('^download/$', views.download, name='lbattachment_download'),
)
