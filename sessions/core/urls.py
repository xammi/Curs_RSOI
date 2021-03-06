from django.conf.urls import url

from core.views import *

urlpatterns = [
    url('^user/identify/$', IdentifyView.as_view()),
    url('^user/authenticate/$', AuthenticateView.as_view()),
    url('^user/create/$', CreateUserView.as_view()),
]
