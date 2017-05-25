from django.http import JsonResponse
from django.views import View


class CreateDisplayView(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        return JsonResponse({'status': 'OK'})


class CreateTransitView(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        return JsonResponse({'status': 'OK'})


class StatView(View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        return JsonResponse({'status': 'OK'})
