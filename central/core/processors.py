from django.conf import settings


def service_domains(request):
    return {
        'target_domain': settings.TARGET_URL,
        'site_url': settings.SITE_URL,
    }


def is_authenticated(request):
    session = request.session
    if not session.get('authorized'):
        return {}

    return {
        'user_authorized': True,
        'user_email': session.get('email'),
    }
