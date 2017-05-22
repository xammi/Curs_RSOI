import uuid

from django.db import models


class DefaultModel(models.Model):
    class Meta:
        abstract = True

    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлено в')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано в')
    is_active = models.BooleanField(default=True, verbose_name='Активно?')


class ACompany(DefaultModel):
    class Meta:
        verbose_name = 'Рекламная кампания'
        verbose_name_plural = 'рекламные кампании'
        ordering = ['-created']

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(verbose_name='Название продукта', max_length=100)
    text = models.TextField(verbose_name='Текст', max_length=300)
    owner = models.CharField(verbose_name='Владелец', max_length=64)
    link = models.URLField(max_length=256, verbose_name='Ссылка перехода', blank=True, null=True)
    max_score = models.PositiveIntegerField(verbose_name='Макс. траты в неделю', blank=True, null=True)

    def __str__(self):
        return self.title

    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'text': self.text,
            'link': self.link,
            'max_score': self.max_score,
            'owner': self.owner,
        }


class ImageAttachment(DefaultModel):
    class Meta:
        verbose_name = 'Картинка'
        verbose_name_plural = 'картинки'
        ordering = ['-weight']

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('ACompany', verbose_name='Рекламная компания')
    image = models.ImageField(verbose_name='Файл картинки', upload_to='images')
    weight = models.IntegerField(verbose_name='Вес картинки', default=1)

    def __str__(self):
        return '{} Image {}'.format(self.company, self.id)

    def as_dict(self):
        return {
            'id': self.id,
            'url': self.image.url,
        }


class ASite(DefaultModel):
    FORUM = 0
    INFO_SITE = 1
    SHOP = 2
    SOCIAL_NET = 3
    GAME = 4
    TOOL = 5
    BLOG = 6

    TOPICS = (
        (FORUM, 'Форум'),
        (INFO_SITE, 'Сайт-визитка'),
        (SHOP, 'Интернет-магазин'),
        (SOCIAL_NET, 'Социальная сеть'),
        (GAME, 'Игра'),
        (TOOL, 'Инструмент'),
        (BLOG, 'Блог'),
    )

    class Meta:
        verbose_name = 'Рекламная площадка'
        verbose_name_plural = 'рекламные площадки'
        ordering = ['-created']

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(verbose_name='Название сайта', max_length=100)
    topic = models.PositiveIntegerField(verbose_name='Тип площадки', choices=TOPICS)
    link = models.URLField(max_length=256, verbose_name='Домен сайта')
    owner = models.CharField(verbose_name='Владелец', max_length=64)

    def __str__(self):
        return self.title

    def get_human_topic(self):
        if self.topic is not None and self.topic in self.TOPICS:
            return dict(self.TOPICS).get(self.topic)
        return 'Тип неизвестен'

    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'topic': self.get_human_topic(),
            'link': self.link,
            'owner': self.owner,
        }
