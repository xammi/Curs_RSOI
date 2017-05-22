from django.conf.urls import url

from grant.views import TokenView

urlpatterns = [
    url('^app/token/$', TokenView.as_view()),
]
