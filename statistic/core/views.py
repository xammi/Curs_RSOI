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

    @classmethod
    def get_datetime_fmt(cls, group_by):
        if group_by == 'minute':
            return '%d.%m.%Y %H:%M'
        elif group_by == 'hour':
            return '%d.%m.%Y %H'
        elif group_by == 'day':
            return '%d.%m.%Y'
        return '%d.%m.%Y %H:%M:%S'

    @staticmethod
    def collect_kwargs(request, names, prefix=''):
        kwargs = {}
        for name in names:
            value = request.GET.get(name)
            if value:
                kwargs[prefix + name] = value
        return kwargs

    @classmethod
    def collect_groups(cls, data, group_by):
        groups = {}
        fmt = cls.get_datetime_fmt(group_by)
        for item in data:
            date = item.accepted.strftime(fmt)
            if date not in groups:
                groups[date] = {'cnt': 0, 'items': []}
            groups[date]['cnt'] += 1

            item_stat = item.as_stat()
            if item_stat:
                groups[date]['items'].append(item_stat)
        return groups

    def get(self, request, *args, **kwargs):
        group_by = request.GET.get('group', 'minute')

        filter_kwargs = self.collect_kwargs(request, self.filter_by)
        displays = Display.objects.filter(**filter_kwargs)

        filter_kwargs = self.collect_kwargs(request, self.filter_by, prefix='display__')
        transits = Transit.objects.filter(**filter_kwargs)

        stat = {
            'transits': self.collect_groups(transits, group_by),
            'displays': self.collect_groups(displays, group_by),
        }
        return JsonResponse({'status': 'OK', 'stat': stat})
