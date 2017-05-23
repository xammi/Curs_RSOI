from django import forms
from django.contrib.messages import add_message, ERROR
from django.core.exceptions import ValidationError
from django.http import HttpResponseForbidden, HttpResponseNotFound, HttpResponse, HttpResponseBadRequest
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, DetailView, FormView, RedirectView
from requests import ReadTimeout, ConnectionError

from core.access import SessionsAccessor, TargetAccessor, StatisticAccessor


ADVISER = 'Рекламодатель'
SITE_OWNER = 'Владелец сайта'

TOPICS = (
    (0, 'Форум'),
    (1, 'Сайт-визитка'),
    (2, 'Интернет-магазин'),
    (3, 'Социальная сеть'),
    (4, 'Игра'),
    (5, 'Инструмент'),
    (6, 'Блог'),
)


class LoginRequiredMixin:
    user_id = None

    def dispatch(self, request, *args, **kwargs):
        session = request.session
        if not session.get('authorized'):
            return HttpResponseForbidden()
        self.user_id = session.get('user_id')
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
        context['ADVISER'] = 0  # ADVISER
        context['SITE_OWNER'] = 1  # SITE_OWNER
        return context


class LoginView(AjaxFormView):
    class AuthForm(forms.Form):
        email = forms.EmailField(max_length=128)
        password = forms.CharField(max_length=128)

    http_method_names = ['post']
    form_class = AuthForm

    def form_valid(self, form):
        try:
            auth_data = SessionsAccessor.send_request('/user/authenticate/', form.cleaned_data)
            if auth_data:
                if auth_data.get('status') == 'OK':
                    session = self.request.session
                    session['authorized'] = True
                    session['user_id'] = auth_data.get('data')
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
        if 'user_id' in session:
            del session['user_id']
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
            result = SessionsAccessor.send_request('/user/identify/', {'id': self.user_id}, method='get')
            self.object = result if result else None
        except (ConnectionError, ReadTimeout):
            add_message(request, ERROR, u'Сервис sessions в данный момент недоступен')
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.object:
            context.update(self.object)
            role = self.object.get('role')
            params = {'owner': self.user_id}

            if role == ADVISER:
                try:
                    result = TargetAccessor.send_request('/company/list/', params, method='get')
                    context['my_companies'] = result.get('data')
                except (ConnectionError, ReadTimeout):
                    add_message(self.request, ERROR, u'Сервис target в данный момент недоступен')

            elif role == SITE_OWNER:
                try:
                    result = TargetAccessor.send_request('/site/list/', params, method='get')
                    context['my_sites'] = result.get('data')
                except (ConnectionError, ReadTimeout):
                    add_message(self.request, ERROR, u'Сервис target в данный момент недоступен')

        context['SITE_TOPICS'] = TOPICS
        context['ADVISER'] = ADVISER
        context['SITE_OWNER'] = SITE_OWNER
        return context


class RegisterView(AjaxFormView):
    http_method_names = ['post']

    class RegisterForm(forms.Form):
        email = forms.EmailField(max_length=128)
        first_name = forms.CharField(max_length=128, required=False)
        last_name = forms.CharField(max_length=128, required=False)
        role = forms.ChoiceField(choices=((0, ADVISER), (1, SITE_OWNER)))

        password = forms.CharField(max_length=128)
        confirm = forms.CharField(max_length=128)

        def clean(self):
            cleaned_data = super().clean()
            password, confirm = cleaned_data.get('password'), cleaned_data.get('confirm')
            if password != confirm:
                raise ValidationError({'confirm': 'Пароли не совпадают'})
            return cleaned_data

    form_class = RegisterForm

    def dispatch(self, request, *args, **kwargs):
        if request.session.get('authorized'):
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            result = SessionsAccessor.send_request('/user/create/', form.cleaned_data)
            if result.get('status') != 'OK':
                return JsonResponse({'status': self.error_status, 'errors': result.get('errors')})

        except (ConnectionError, ReadTimeout):
            return JsonResponse({
                'status': self.error_status,
                'errors': {'email': 'Сервис sessions в данный момент не доступен'},
            })

        if result.get('status') == 'OK':
            session = self.request.session
            session['authorized'] = True
            session['user_id'] = result.get('data', {}).get('id')
            session['email'] = result.get('data', {}).get('email')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('core:profile')


class AddSiteView(LoginRequiredMixin, AjaxFormView):
    http_method_names = ['post']

    class AddSiteForm(forms.Form):
        topic = forms.ChoiceField(choices=TOPICS)
        title = forms.CharField(max_length=100)
        link = forms.URLField(max_length=256)

    form_class = AddSiteForm

    def form_valid(self, form):
        form.cleaned_data['owner'] = self.user_id
        try:
            result = TargetAccessor.send_request('/site/create/', form.cleaned_data)
            if result.get('status') != 'OK':
                return JsonResponse({'status': self.error_status, 'errors': result.get('errors')})

            site_data = result.get('data')
            site_data['details_url'] = reverse('core:site_details', args=[site_data.get('id')])
            return JsonResponse({'status': self.ok_status, 'data': site_data})

        except (ConnectionError, ReadTimeout):
            return JsonResponse({
                'status': 'ERROR',
                'errors': {'title': 'Сервис target в данный момент не доступен'},
            })


class AddCompanyView(LoginRequiredMixin, AjaxFormView):
    http_method_names = ['post']

    class AddCompanyForm(forms.Form):
        title = forms.CharField(max_length=100)
        text = forms.CharField(max_length=300)
        link = forms.URLField(max_length=256)
        max_score = forms.IntegerField(min_value=0)

    form_class = AddCompanyForm

    def form_valid(self, form):
        form.cleaned_data['owner'] = self.user_id
        try:
            result = TargetAccessor.send_request('/company/create/', form.cleaned_data)
            if result.get('status') != 'OK':
                return JsonResponse({'status': self.error_status, 'errors': result.get('errors')})

            company_data = result.get('data')
            company_data['details_url'] = reverse('core:company_details', args=[company_data.get('id')])
            return JsonResponse({'status': self.ok_status, 'data': company_data})

        except (ConnectionError, ReadTimeout):
            return JsonResponse({
                'status': 'ERROR',
                'errors': {'title': 'Сервис target в данный момент не доступен'},
            })


class ProxyDetailView(LoginRequiredMixin, TemplateView):
    http_method_names = ['get']
    context_object_name = None
    pk_url_name = None
    target_route = None

    def get_object(self, **kwargs):
        uuid = kwargs.get(self.pk_url_name)
        try:
            return TargetAccessor.send_request(self.target_route.format(uuid), {}, method='get')
        except (ConnectionError, ReadTimeout):
            add_message(self.request, ERROR, u'Сервис target в данный момент недоступен')

    def get(self, request, *args, **kwargs):
        object = self.get_object(**kwargs)
        if not object:
            return HttpResponseNotFound()
        if self.user_id != object.get('owner'):
            return HttpResponseForbidden()
        return super().get(request, *args, object=object, **kwargs)

    def get_context_data(self, object, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.context_object_name] = object
        return context


class SiteDetailView(ProxyDetailView):
    template_name = 'core/concrete_site.html'
    context_object_name = 'site'
    pk_url_name = 'site_id'
    target_route = '/site/{}/'


class CompanyDetailView(ProxyDetailView):
    template_name = 'core/concrete_company.html'
    context_object_name = 'company'
    pk_url_name = 'company_id'
    target_route = '/company/{}/'


class AddImageView(LoginRequiredMixin, View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        uuid = kwargs.get('company_id')
        image = request.FILES.get('image[]')
        if not image or not uuid:
            return HttpResponseBadRequest()

        try:
            result = TargetAccessor.send_request('/image/create/', {'company': uuid, 'owner': self.user_id}, file=image)
            if not result:
                return HttpResponseBadRequest()

            if result.get('status') == 'OK':
                return JsonResponse({'status': 'OK'})

            error = list(result.get('errors', {}).items())
            if error:
                return JsonResponse({'error': '{}: {}'.format(*error[0])})

        except (ConnectionError, ReadTimeout):
            return JsonResponse({'error': 'Сервис target в данный момент не доступен'})


class DropImageView(LoginRequiredMixin, View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        uuid = kwargs.get('image_id')
        if not uuid:
            return HttpResponseBadRequest()

        try:
            result = TargetAccessor.send_request('/image/delete/', {'image': uuid, 'owner': self.user_id})
            if not result:
                return HttpResponseBadRequest()
            return JsonResponse({'status': 'OK'})

        except (ConnectionError, ReadTimeout):
            return JsonResponse({'error': 'Сервис target в данный момент не доступен'})


class SaveKeywordsView(LoginRequiredMixin, View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        uuid = kwargs.get('site_id')

        data = {'site': uuid, 'owner': self.user_id}
        for part in ['why', 'who', 'what']:
            data[part] = request.POST.get(part)

        try:
            TargetAccessor.send_request('/keywords/save/', data)
            return JsonResponse({'status': 'OK'})

        except (ConnectionError, ReadTimeout):
            return JsonResponse({'error': 'Сервис target в данный момент не доступен'})


class DemoView(TemplateView):
    http_method_names = ['get']
    template_name = 'core/demo.html'

    def get(self, request, *args, **kwargs):
        current = request.GET.get('current', 1)
        try:
            current = int(current)
        except (ValueError, TypeError):
            current = 1
        return super().get(request, *args, current=current, **kwargs)

    def get_context_data(self, current, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current'] = current
        try:
            result = TargetAccessor.send_request('/site/list/', {}, method='get')
            context['sites'] = result.get('data')
            for index, site in enumerate(context['sites']):
                site['current'] = index + 1

            context['sites_cnt'] = len(result.get('data'))
            context['current_site'] = context['sites'][current - 1]
            context['prev'] = current - 1
            context['next'] = current + 1
        except (ConnectionError, ReadTimeout):
            add_message(self.request, ERROR, u'Сервис target в данный момент недоступен')
        return context


class AdvertiseView(View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        return JsonResponse({})
