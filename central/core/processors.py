def is_authenticated(request):
    session = request.session
    if not session.get('authorized'):
        return {}

    return {
        'user_authorized': True,
        'user_email': session.get('email'),
    }
