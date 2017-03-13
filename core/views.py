from django import forms
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.views.generic import TemplateView, DetailView, FormView, RedirectView

from core.models import User


class AjaxFormView(FormView):
    ok_status = 'OK'
    error_status = 'ERROR'

    def form_valid(self, form):
        return JsonResponse({
            'status': self.ok_status,
            'success_url': self.get_success_url(),
        })

    def form_invalid(self, form):
        return JsonResponse({
            'status': self.error_status,
            'errors': form.errors
        })


class IndexView(TemplateView):
    http_method_names = ['get']
    template_name = 'core/index.html'

    def get(self, request, *args, **kwargs):
        # if request.user.is_authenticated():
        #     return HttpResponseRedirect(reverse('core:profile'))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ADVISER'] = User.ADVISER
        context['SITE_OWNER'] = User.SITE_OWNER
        return context


class LoginView(AjaxFormView):
    class AuthForm(forms.Form):
        email = forms.EmailField(max_length=128)
        password = forms.CharField(max_length=128)

    http_method_names = ['post']
    form_class = AuthForm

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            if user.is_active:
                login(self.request, user)
                return super().form_valid(form)
            else:
                error_msg = 'Ваш аккаунт не активирован'
        else:
            error_msg = 'Введены неправильные email или пароль'

        return JsonResponse({
            'status': self.error_status,
            'errors': error_msg
        })

    def get_success_url(self):
        return reverse('core:profile')


class LogoutView(RedirectView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse('core:home')


class ProfileView(LoginRequiredMixin, DetailView):
    http_method_names = ['get']
    template_name = 'core/profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ADVISER'] = User.ADVISER
        context['SITE_OWNER'] = User.SITE_OWNER
        return context


class RegisterView(AjaxFormView):
    class RegisterForm(forms.ModelForm):
        password = forms.CharField(max_length=128)
        confirm = forms.CharField(max_length=128)

        class Meta:
            model = User
            fields = ('email', 'first_name', 'last_name', 'role')

        def clean(self):
            cleaned_data = super().clean()
            password, confirm = cleaned_data.get('password'), cleaned_data.get('confirm')
            if password != confirm:
                raise ValidationError({'confirm': 'Пароли не совпадают'})
            return cleaned_data

        def save(self, commit=True):
            instance = super().save(commit=False)
            instance.email = User.objects.normalize_email(self.cleaned_data.get('email'))
            instance.set_password(self.cleaned_data.get('password'))
            if commit:
                instance.save()
            return instance

    http_method_names = ['post']
    form_class = RegisterForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.is_active = True
        instance.save()
        login(self.request, instance)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('core:profile')
