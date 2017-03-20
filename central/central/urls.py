from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^ssadmin/', admin.site.urls),
    url(r'^', include('core.urls', namespace='core')),
]
