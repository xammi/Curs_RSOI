from django.conf.urls import url

from core.views import IndexView

urlpatterns = [
    url('^$', IndexView.as_view(), name='home'),
]
