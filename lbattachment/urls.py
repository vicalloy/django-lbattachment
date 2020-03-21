from django.urls import path

from . import views

urlpatterns = [
    path('upload__/', views.upload__, name='lbattachment_upload__'),
    path('delete__/', views.delete__, name='lbattachment_delete__'),
    path('change_descn__/', views.change_descn__, name='lbattachment_change_descn__'),
    path('download/', views.download, name='lbattachment_download'),
]
