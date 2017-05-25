from django.conf.urls import url
from django.contrib import admin

from core.views import StatView, CreateTransitView, CreateDisplayView

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^display/create/$', CreateDisplayView.as_view()),
    url(r'^transit/create/$', CreateTransitView.as_view()),

    url(r'stat/', StatView.as_view()),
]
