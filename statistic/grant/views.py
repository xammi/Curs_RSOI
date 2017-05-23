from django.conf import settings
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponseForbidden
from django.utils import timezone
from django.views import View

from grant.models import TemporalGrant


class TokenView(View):
    http_method_names = ['post']
    grant_type = 'client_credentials'

    def post(self, request, *args, **kwargs):
        client_grant_type = request.POST.get('grant_type')
        if client_grant_type != self.grant_type:
            return HttpResponseBadRequest()

        client_id = request.POST.get('client_id')
        app_data = settings.EXTERNAL_ACCESS.get(client_id)
        if not app_data:
            return JsonResponse(TemporalGrant.generate())

        client_secret = request.POST.get('client_secret')
        app_real_secret = app_data.get('client_secret')
        if app_real_secret != client_secret:
            return JsonResponse(TemporalGrant.generate())

        result = TemporalGrant.generate()
        TemporalGrant(**result, app_name=app_data.get('name')).save()
        return JsonResponse(result)


class CheckGrantMixin(object):
    grant_type = TemporalGrant.BEARER_TYPE

    def has_access(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header.startswith('Bearer'):
            return HttpResponseBadRequest()

        token = auth_header[7:]
        now = timezone.now()
        return TemporalGrant.objects.filter(access_token=token, expires_in__gt=now).exists()

    def dispatch(self, request, *args, **kwargs):
        if not self.has_access(request):
            return HttpResponseForbidden()
        return super(CheckGrantMixin, self).dispatch(request, *args, **kwargs)
