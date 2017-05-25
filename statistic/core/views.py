from django import forms
from django.http import JsonResponse
from django.views import View

from core.models import Display, Transit
from grant.views import CheckGrantMixin


class CreateDisplayView(CheckGrantMixin, View):
    http_method_names = ['post']

    class CreateForm(forms.ModelForm):
        class Meta:
            model = Display
            fields = ('site', 'company', 'image', 'user_agent', 'accepted')

    def post(self, request, *args, **kwargs):
        form = CreateDisplayView.CreateForm(request.POST)
        if form.is_valid():
            instance = form.save()
            return JsonResponse({'status': 'OK', 'id': instance.id})
        return JsonResponse({'status': 'ERROR', 'errors': form.errors})


class CreateTransitView(CheckGrantMixin, View):
    http_method_names = ['post']

    class CreateForm(forms.ModelForm):
        class Meta:
            model = Transit
            fields = ('display', 'accepted')

    def post(self, request, *args, **kwargs):
        print(request.POST)
        form = CreateTransitView.CreateForm(request.POST)
        if form.is_valid():
            instance = form.save()
            return JsonResponse({'status': 'OK', 'id': instance.id})
        print(form.errors)
        return JsonResponse({'status': 'ERROR', 'errors': form.errors})


class StatView(CheckGrantMixin, View):
    http_method_names = ['get']
    filter_by = ('company', 'site')
    extractor = lambda x: x.accepted.strftime('%d.%m.%Y %H:%M:%S')

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
        transits = Transit.objects.filter(**filter_kwargs)
        displays = Display.objects.filter(**filter_kwargs)
        stat = {
            'transits': list(map(self.extractor, transits)),
            'displays': list(map(self.extractor, displays)),
        }
        return JsonResponse({'status': 'OK', 'stat': stat})
