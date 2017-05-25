import uuid

from django.db import models


class Display(models.Model):
    class Meta:
        verbose_name = 'Показ'
        verbose_name_plural = 'показы'
        ordering = ['-accepted']

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.UUIDField(verbose_name='ID компании')
    image = models.UUIDField(verbose_name='ID картинки', null=True, blank=True)

    site = models.UUIDField(verbose_name='ID площадки')
    accepted = models.DateTimeField(verbose_name='Время создания')
    user_agent = models.CharField(verbose_name='User-agent', max_length=256, null=True, blank=True)

    def __unicode__(self):
        return 'Показ ID={}'.format(self.id)

    def parse_user_agent(self):
        pass

    def as_stat(self):
        return {}


class Transit(models.Model):
    class Meta:
        verbose_name = 'Переход по рекламе'
        verbose_name_plural = 'переходы по рекламе'
        ordering = ['-accepted']

    display = models.ForeignKey('Display', verbose_name='Показ')
    accepted = models.DateTimeField(verbose_name='Время создания')

    def __unicode__(self):
        return 'Переход ID={}'.format(self.id)

    def as_stat(self):
        return {}
