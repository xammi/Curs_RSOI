from django.conf.urls import url

from core.views import IndexView, ProfileView, LoginView, LogoutView, RegisterView

urlpatterns = [
    url('^$', IndexView.as_view(), name='home'),
    url('^index/$', IndexView.as_view(), name='index'),

    url('^profile/$', ProfileView.as_view(), name='profile'),
    url('^login/$', LoginView.as_view(), name='login'),
    url('^logout/$', LogoutView.as_view(), name='logout'),
    url('^register/$', RegisterView.as_view(), name='register')
]
