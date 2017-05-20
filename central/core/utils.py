from urllib.parse import urljoin

import requests
from django.conf import settings
from django.utils import timezone


class SessionsAccessor:
    client_id = settings.SESSIONS_ID
    client_secret = settings.SESSIONS_SECRET
    service_url = settings.SESSIONS_URL
    prev_token = {'access_token': '', 'expires_in': None}

    @classmethod
    def is_token_actual(cls):
        prev_expires = cls.prev_token.get('expires_in')
        return prev_expires and timezone.now() < prev_expires

    @classmethod
    def get_ask_data(cls):
        return {
            'grant_type': 'client_credentials',
            'client_id': cls.client_id,
            'client_secret': cls.client_secret,
        }

    @classmethod
    def get_token_url(cls):
        return urljoin(cls.service_url, '/app/token/')

    @classmethod
    def get_token(cls):
        if cls.is_token_actual():
            return cls.prev_token.get('access_token')

        grant_url = cls.get_token_url()
        grant_data = cls.get_ask_data()
        response = requests.post(grant_url, data=grant_data, timeout=2)

        if response.status_code != 200:
            print('Error when getting sessions token: code={}'.format(response))
            raise ConnectionError(response.status_code)

        cls.prev_token = response.content
        return cls.prev_token.get('access_token')

    @classmethod
    def send_request(cls, method, data):
        token = cls.get_token()

        auth_url = urljoin(settings.SESSIONS_URL, '/user/', method)
        auth_headers = {'Authorization': 'Bearer:{0}'.format(token)}

        response = requests.post(auth_url, headers=auth_headers, data=data, timeout=2)
        if response.status_code == 404:
            return None

        elif response.status_code != 200:
            print('Error when authorizing: code={}'.format(response))
            raise ConnectionError(response.status_code)

        return response.content
