from django import forms
from django.db.models import Count
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.utils import timezone
from django.views import View

from core.models import ASite, ACompany, ImageAttachment
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

    def extra_data(self, obj):
        return {}

    def get(self, request, *args, **kwargs):
        obj_id = kwargs.get(self.pk_url_name)
        if not obj_id:
            return HttpResponseBadRequest()

        obj = self.model.objects.filter(id=obj_id).first()
        if not obj:
            return HttpResponseNotFound()

        result = obj.as_dict()
        result.update(self.extra_data(obj))
        return JsonResponse(result)


class SiteDetailView(DetailView):
    model = ASite


class CompanyDetailView(DetailView):
    model = ACompany

    def extra_data(self, obj):
        return {'images': [
            i.as_dict() for i in obj.imageattachment_set.all()
        ]}


class CreateImageView(CheckGrantMixin, View):
    http_method_names = ['post']

    class CreateForm(forms.ModelForm):
        class Meta:
            model = ImageAttachment
            fields = ('company', 'image')

    def post(self, request, *args, **kwargs):
        form = CreateImageView.CreateForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            # check ownership before add
            image = form.save()
            return JsonResponse({'status': 'OK', 'image_url': image.image.url})
        return JsonResponse({'status': 'ERROR', 'errors': form.errors})


class DeleteImageView(CheckGrantMixin, View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        image_id = request.POST.get('image')
        if not image_id:
            return HttpResponseBadRequest()

        ImageAttachment.objects.filter(id=image_id).delete()
        return JsonResponse({'status': 'OK'})


class SaveKeywords(CheckGrantMixin, View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        site_id = request.POST.get('site')
        if not site_id:
            return HttpResponseBadRequest()

        site = ASite.objects.filter(id=site_id).first()
        if not site:
            return HttpResponseNotFound()

        was_changed = False
        for type in ['why', 'who', 'what']:
            words = request.POST.get(type)
            if words:
                setattr(site, type + '_words', words)
                was_changed = True

        if was_changed:
            site.save()
        return JsonResponse({'status': 'OK'})


class AdvertiseView(View):
    http_method_names = ['get']

    def choose_adv(self, site, request, now):
        companies = ACompany.objects.annotate(image_cnt=Count('imageattachment')).order_by('-image_cnt')
        return companies.first()

    def get(self, request, *args, **kwargs):
        now = timezone.now()
        site_id = request.GET.get('site')
        if not site_id:
            return HttpResponseBadRequest()

        site = ASite.objects.filter(id=site_id).first()
        if not site:
            return HttpResponseNotFound()

        company = self.choose_adv(site, request.META, now)
        if not company:
            return HttpResponseNotFound()

        adv = company.as_adv_data()
        adv['site'] = site.as_dict()
        return JsonResponse(adv)
