from django import forms
from django.contrib.auth import authenticate
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound
from django.views import View

from core.models import User
from grant.views import CheckGrantMixin


class IdentifyView(CheckGrantMixin, View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        user_id = request.GET.get('id')
        if not user_id:
            return HttpResponseBadRequest()

        user = User.objects.filter(id=user_id).first()
        if not user:
            return HttpResponseNotFound()
        return JsonResponse(user.as_dict())


class AuthenticateView(CheckGrantMixin, View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not email or not password:
            return HttpResponseBadRequest()

        user = authenticate(email=email, password=password)
        if user:
            if user.is_active:
                return JsonResponse({'status': 'OK', 'data': user.id})
            return JsonResponse({'status': 'NOT ACTIVE'})
        return HttpResponseNotFound()


class CreateUserView(CheckGrantMixin, View):
    http_method_names = ['post']

    class RegisterForm(forms.ModelForm):
        class Meta:
            model = User
            fields = ('email', 'first_name', 'last_name', 'role')
        password = forms.CharField(max_length=128)

    def post(self, request, *args, **kwargs):
        form = CreateUserView.RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(**form.cleaned_data, is_active=True)
            return JsonResponse({'status': 'OK', 'data': user.as_dict()})
        return JsonResponse({'status': 'ERROR', 'errors': form.errors})


