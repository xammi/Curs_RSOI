from django.conf.urls import url

from core.views import CreateSiteView, CreateCompanyView, SiteListView, CompanyListView, SiteDetailView, \
    CompanyDetailView

urlpatterns = [
    url(r'^site/create/$', CreateSiteView.as_view()),
    url(r'^site/list/$', SiteListView.as_view()),
    url(r'^site/(?P<uuid>[\w\d\-]+)/$', SiteDetailView.as_view()),

    url(r'^company/create/$', CreateCompanyView.as_view()),
    url(r'^company/list/$', CompanyListView.as_view()),
    url(r'^company/(?P<uuid>[\w\d\-]+)/$', CompanyDetailView.as_view()),
]
