import base64
import binascii

from urllib.parse import unquote_plus
from django import forms
from django.contrib.auth import authenticate
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound
from django.views import View

from core.models import User, TemporalGrant
from sessions.settings import EXTERNAL_ACCESS


class TokenView(View):
    http_method_names = ['POST']
    grant_type = 'client_credentials'

    def post(self, request, *args, **kwargs):
        client_grant_type = request.POST.get('grant_type')
        if client_grant_type != self.grant_type:
            return HttpResponseBadRequest()

        client_id = request.POST.get('client_id')
        app_data = EXTERNAL_ACCESS.get(client_id)
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
        auth_string = request.META.get('HTTP_AUTHORIZATION')
        auth_parts = auth_string.split(' ', 1)
        if len(auth_parts) != 2:
            return False

        client_grant_type, auth_string = auth_parts
        if client_grant_type != self.grant_type:
            return False

        try:
            b64_dec = base64.b64decode(auth_string)
        except (TypeError, binascii.Error):
            return False

        try:
            encoding = request.charset if hasattr(request, 'charset') else 'utf-8'
            auth_decoded = b64_dec.decode(encoding)
        except UnicodeDecodeError:
            return False

        client_id, client_secret = map(unquote_plus, auth_decoded.split(':', 1))
        app_data = EXTERNAL_ACCESS.get(client_id)
        app_real_secret = app_data.get('client_secret')
        return app_real_secret == client_secret

    def dispatch(self, request, *args, **kwargs):
        if not self.has_access(request):
            return HttpResponseForbidden()
        return super(CheckGrantMixin, self).dispatch(request, *args, **kwargs)


class IdentifyView(CheckGrantMixin, View):
    http_method_names = ['GET']

    def get(self, request, *args, **kwargs):
        email = request.GET.get('email')
        if not email:
            return HttpResponseBadRequest()

        user = User.objects.filter(email=email).first()
        if not user:
            return HttpResponseNotFound()
        return JsonResponse(user.as_dict())


class AuthenticateView(CheckGrantMixin, View):
    http_method_names = ['POST']

    def post(self, request, *args, **kwargs):
        email = request.GET.get('email')
        password = request.GET.get('password')
        if not email or not password:
            return HttpResponseBadRequest()

        user = authenticate(email=email, password=password)
        if user:
            if user.is_active:
                return JsonResponse({'status': 'OK'})
            return JsonResponse({'status': 'NOT ACTIVE'})
        return HttpResponseNotFound()


class CreateUserView(CheckGrantMixin, View):
    http_method_names = ['POST']

    class RegisterForm(forms.ModelForm):
        class Meta:
            model = User
            fields = ('email', 'first_name', 'last_name', 'role')
        password = forms.CharField(max_length=128)

    def post(self, request, *args, **kwargs):
        form = CreateUserView.RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(**form.cleaned_data, is_active=True)
            return JsonResponse({'status': 'OK', 'data': user.as_json()})
        return JsonResponse({'status': 'ERROR', 'errors': form.errors})


