from django.conf.urls import url

from core.views import CreateSiteView

urlpatterns = [
    url(r'^site/create/', CreateSiteView.as_view()),
]
