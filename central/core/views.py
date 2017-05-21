from django import forms
from django.core.exceptions import ValidationError
from django.http import HttpResponseForbidden
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView, DetailView, FormView, RedirectView
from requests import ReadTimeout, ConnectionError

from core.models import User, ACompany, ASite
from core.utils import SessionsAccessor


class LoginRequiredMixin:
    user_email = None

    def dispatch(self, request, *args, **kwargs):
        session = request.session
        if not session.get('authorized'):
            return HttpResponseForbidden()
        self.user_email = session.get('email')
        return super().dispatch(request, *args, **kwargs)


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
        try:
            auth_data = SessionsAccessor.send_request('/authenticate/', form.cleaned_data)
            if auth_data:
                if auth_data.get('status') == 'OK':
                    session = self.request.session
                    session['authorized'] = True
                    session['email'] = form.cleaned_data.get('email')
                    return super().form_valid(form)
                else:
                    error_msg = 'Ваш аккаунт не активирован'
            else:
                error_msg = 'Введены неправильные email или пароль'
        except (ConnectionError, ReadTimeout):
            error_msg = 'Сервис sessions в данный момент недоступен'

        return JsonResponse({
            'status': self.error_status,
            'errors': error_msg
        })

    def get_success_url(self):
        return reverse('core:profile')


class LogoutView(RedirectView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        session = self.request.session
        if 'authorized' in session:
            del session['authorized']
        if 'email' in session:
            del session['email']
        return super().get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse('core:home')


class ProfileView(LoginRequiredMixin, DetailView):
    http_method_names = ['get']
    template_name = 'core/profile.html'
    context_object_name = 'user'

    def get(self, request, *args, **kwargs):
        try:
            self.object = None
            result = SessionsAccessor.send_request('/identify/', {'email': self.user_email})
            self.object = result if result else None
        except (ConnectionError, ReadTimeout):
            pass
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.object:
            context.update(self.object)

        role = context.get('role')
        if role == User.ADVISER:
            context['my_companies'] = ACompany.objects.all()
        elif role == User.SITE_OWNER:
            context['my_sites'] = ASite.objects.all()

        context['SITE_TOPICS'] = ASite.TOPICS
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

    http_method_names = ['post']
    form_class = RegisterForm

    def dispatch(self, request, *args, **kwargs):
        if request.session.get('authorized'):
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            result = SessionsAccessor.send_request('/create/', form.cleaned_data)
            if result.get('status') != 'OK':
                return JsonResponse({
                    'status': self.error_status,
                    'errors': result.get('errors'),
                })

        except (ConnectionError, ReadTimeout):
            return JsonResponse({
                'status': self.error_status,
                'errors': 'Сервис sessions в данный момент не доступен'
            })

        session = self.request.session
        session['authorized'] = True
        session['email'] = form.cleaned_data.get('email')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('core:profile')


class AddSiteView(AjaxFormView):
    class AddSiteForm(forms.ModelForm):
        class Meta:
            model = ASite
            fields = ('title', 'link', 'topic')

        def __init__(self, user, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.user = user

        def save(self, commit=True):
            instance = super().save(commit=False)
            instance.owner = self.user
            if commit:
                instance.save()
            return instance

    http_method_names = ['post']
    form_class = AddSiteForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        instance = form.save()
        return JsonResponse({
            'status': self.ok_status,
            'data': instance.as_json()
        })


class SiteDetailView(LoginRequiredMixin, DetailView):
    http_method_names = ['get']
    model = ASite
    pk_url_kwarg = 'site_id'
    context_object_name = 'site'
    template_name = 'core/concrete_site.html'

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.owner:
            return HttpResponseForbidden()
        return super().get(request, *args, **kwargs)


class AddCompanyView(AjaxFormView):
    class AddCompanyForm(forms.ModelForm):
        class Meta:
            model = ACompany
            fields = ('title', 'text', 'link', 'max_score')

        def __init__(self, user, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.user = user

        def save(self, commit=True):
            instance = super().save(commit=False)
            instance.owner = self.user
            if commit:
                instance.save()
            return instance

    http_method_names = ['post']
    form_class = AddCompanyForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        instance = form.save()
        return JsonResponse({
            'status': self.ok_status,
            'data': instance.as_json()
        })


class CompanyDetailView(LoginRequiredMixin, DetailView):
    http_method_names = ['get']
    model = ACompany
    pk_url_kwarg = 'company_id'
    context_object_name = 'company'
    template_name = 'core/concrete_company.html'

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.owner:
            return HttpResponseForbidden()
        return super().get(request, *args, **kwargs)
