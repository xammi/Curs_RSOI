from django.conf.urls import url

from core.views import IndexView, ProfileView, LoginView, LogoutView, RegisterView, AddSiteView, SiteDetailView, \
    AddCompanyView, CompanyDetailView, AddImageView, DropImageView, SaveKeywordsView, DemoView, AdvertiseView

urlpatterns = [
    url('^$', IndexView.as_view(), name='home'),
    url('^index/$', IndexView.as_view(), name='index'),
    url('^demo/$', DemoView.as_view(), name='demo'),

    url('^profile/$', ProfileView.as_view(), name='profile'),
    url('^login/$', LoginView.as_view(), name='login'),
    url('^logout/$', LogoutView.as_view(), name='logout'),
    url('^register/$', RegisterView.as_view(), name='register'),

    url('^site/add/$', AddSiteView.as_view(), name='add_site'),
    url('^site/details/(?P<site_id>[\d\w\-]+)/$', SiteDetailView.as_view(), name='site_details'),
    url('^company/add/$', AddCompanyView.as_view(), name='add_company'),
    url('^company/details/(?P<company_id>[\d\w\-]+)/$', CompanyDetailView.as_view(), name='company_details'),

    url('^image/add/(?P<company_id>[\d\w\-]+)/$', AddImageView.as_view(), name='add_image'),
    url('^image/drop/(?P<image_id>[\d\w\-]+)/$', DropImageView.as_view(), name='drop_image'),
    url('^keywords/save/(?P<site_id>[\d\w\-]+)/$', SaveKeywordsView.as_view(), name='save_keywords'),

    url('^adv/', AdvertiseView.as_view(), name='adv'),
]
