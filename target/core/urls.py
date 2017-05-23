from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from core.views import CreateSiteView, CreateCompanyView, SiteListView, CompanyListView, SiteDetailView, \
    CompanyDetailView, CreateImageView, DeleteImageView, SaveKeywords

urlpatterns = [
    url(r'^site/create/$', CreateSiteView.as_view()),
    url(r'^site/list/$', SiteListView.as_view()),
    url(r'^site/(?P<uuid>[\w\d\-]+)/$', SiteDetailView.as_view()),

    url(r'^company/create/$', CreateCompanyView.as_view()),
    url(r'^company/list/$', CompanyListView.as_view()),
    url(r'^company/(?P<uuid>[\w\d\-]+)/$', CompanyDetailView.as_view()),

    url(r'^image/create/$', CreateImageView.as_view()),
    url(r'^image/delete/$', DeleteImageView.as_view()),
    url(r'^keywords/save/$', SaveKeywords.as_view()),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
