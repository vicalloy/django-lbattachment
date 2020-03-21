import django
from django.conf.urls import include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r"^", include("lbattachment.urls")),
]

if django.VERSION < (1, 9, 0):
    urlpatterns.append(
        url(r'^admin/', include(admin.site.urls)),
    )
else:
    urlpatterns.append(
        url(r'^admin/', admin.site.urls),
    )
