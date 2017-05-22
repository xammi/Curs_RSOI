from django import forms
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views import View

from core.models import ASite, ACompany
from grant.views import CheckGrantMixin


class CreateSiteView(CheckGrantMixin, View):
    http_method_names = ['post']

    class CreateForm(forms.ModelForm):
        class Meta:
            model = ASite
            fields = ('title', 'topic', 'link', 'owner')

    def post(self, request, *args, **kwargs):
        form = CreateSiteView.CreateForm(request.POST)
        if form.is_valid():
            site = form.save()
            return JsonResponse({'status': 'OK', 'data': site.as_dict()})
        return JsonResponse({'status': 'ERROR', 'errors': form.errors})


class CreateCompanyView(CheckGrantMixin, View):
    http_method_names = ['post']

    class CreateForm(forms.ModelForm):
        class Meta:
            model = ACompany
            fields = ('title', 'text', 'owner', 'link', 'max_score')

    def post(self, request, *args, **kwargs):
        form = CreateCompanyView.CreateForm(request.POST)
        if form.is_valid():
            company = form.save()
            return JsonResponse({'status': 'OK', 'data': company.as_dict()})
        return JsonResponse({'status': 'ERROR', 'errors': form.errors})


class ListView(CheckGrantMixin, View):
    http_method_names = ['get']
    model = None
    filter_by = ()

    @staticmethod
    def collect_kwargs(request, names):
        kwargs = {}
        for name in names:
            value = request.GET.get(name)
            if value:
                kwargs[name] = value
        return kwargs

    def get(self, request, *args, **kwargs):
        filter_kwargs = self.collect_kwargs(request, self.filter_by)
        obj_list = [
            obj.as_dict() for obj in self.model.objects.filter(**filter_kwargs)
        ]
        return JsonResponse({'data': obj_list})


class SiteListView(ListView):
    model = ASite
    filter_by = ('owner', 'topic', 'link')


class CompanyListView(ListView):
    model = ACompany
    filter_by = ('owner', 'link')


class DetailView(CheckGrantMixin, View):
    http_method_names = ['get']
    pk_url_name = 'uuid'
    model = None

    def get(self, request, *args, **kwargs):
        obj_id = kwargs.get(self.pk_url_name)
        if not obj_id:
            return HttpResponseBadRequest()
        obj = self.model.objects.filter(id=obj_id).first()
        if not obj:
            return HttpResponseNotFound()
        return JsonResponse(obj.as_dict())


class SiteDetailView(DetailView):
    model = ASite


class CompanyDetailView(DetailView):
    model = ACompany
