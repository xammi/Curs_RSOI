import random
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

    def get_random_image(self):
        objects = self.imageattachment_set.all()
        weights = list(map(lambda x: x.weight, objects))

        num = random.randint(1, sum(weights) * 10)
        marker = 0
        for index, weight in enumerate(weights):
            if weight > 0:
                old, marker = marker, marker + weight * 10
                if old < num <= marker:
                    return objects[index]
        return None

    def as_adv_data(self):
        attach = self.get_random_image()
        return {
            'id': self.id,
            'title': self.title,
            'link': self.link,
            'text': self.text,
            'image': attach.as_dict() if attach else {},
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
            'factor': self.get_factor(),
        }

    def get_factor(self):
        width, height = self.image.width, self.image.height
        return float(height) / float(width)


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

    why_words = models.CharField(max_length=256, verbose_name='Для чего?', null=True, blank=True)
    who_words = models.CharField(max_length=256, verbose_name='Для кого?', null=True, blank=True)
    what_words = models.CharField(max_length=256, verbose_name='Что тут делают?', null=True, blank=True)

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
            'why': self.why_words.split(',') if self.why_words else [],
            'who': self.who_words.split(',') if self.who_words else [],
            'what': self.what_words.split(',') if self.what_words else [],
        }
