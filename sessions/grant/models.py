from datetime import timedelta

from django.db import models
from django.utils import timezone

from grant.utils import generate_token


class TemporalGrant(models.Model):
    class Meta:
        verbose_name = 'Токен доступа'
        verbose_name_plural = 'токены доступа'

    BEARER_TYPE = 'Bearer'
    TYPES = (
        (BEARER_TYPE, 'Bearer'),
    )

    access_token = models.CharField(verbose_name='Токен', max_length=64)
    token_type = models.CharField(verbose_name='Тип', max_length=30, choices=TYPES)
    expires_in = models.DateTimeField(verbose_name='Протухнет в')
    app_name = models.CharField(verbose_name='Приложение', max_length=30)

    @classmethod
    def generate(cls):
        return {
            'token_type': cls.BEARER_TYPE,
            'expires_in': timezone.now() + timedelta(seconds=1000),
            'access_token': generate_token(),
        }

    def __unicode__(self):
        return self.access_token
