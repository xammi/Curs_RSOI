"""
Django settings for untitled project.

Generated by 'django-admin startproject' using Django 1.10.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^le&_l*z7nyy%eroj-^dtlcb4pv=l8_hwgw_mls=)hq&jf^u#u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['95.163.32.114']

SITE_URL = 'http://95.163.32.114:8003'

EXTERNAL_ACCESS = {
    'fNdWPYKhXnnuxFiFVByOzOyqlTZrDynqKZtAHmmA': {
        'name': 'central',
        'client_id': 'fNdWPYKhXnnuxFiFVByOzOyqlTZrDynqKZtAHmmA',
        'client_secret': 'zhZuvixkqtcQigPIRSTcSjesNfrodWDognFKLRXfZprlNHnGkVYlcfsOyzJMdxXsSSQtJPELBKgtThRIUfGhGEGfEGPGRWcgnRBIXtNGiNEYiepfTPiJFnxZlPPWALVa',
    },
    'JiZVrthIgyXeJjcigfujNAdRrgqizPDkJgAmyLvy': {
        'name': 'target',
        'client_id': 'JiZVrthIgyXeJjcigfujNAdRrgqizPDkJgAmyLvy',
        'client_secret': 'ZqUcuwOCBSmlsQmLmgbOHozXrfyrVVoVBQHexrNXOuyyqdhrvgmNCuwfvgxjvkFJmetABFzDpnrctTKLmtQMVGssOCjBSFFYPehQaAZKdRcwdIfNeVJvkwGYUjebLUDy',
    },
}


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
] + [
    'core',
    'grant',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'statistic.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'statistic.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

try:
    from .local_settings import *
except ImportError:
    pass
