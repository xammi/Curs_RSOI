from django.http import JsonResponse
from django.views import View


class CreateSiteView(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        return JsonResponse({})
