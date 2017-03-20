from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.urls import reverse


class DefaultModel(models.Model):
    class Meta:
        abstract = True

    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлено в')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано в')
    is_active = models.BooleanField(default=True, verbose_name='Активно?')


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')

        if 'username' in extra_fields:
            del extra_fields['username']

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields['is_active'] = True
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ADVISER = 0
    SITE_OWNER = 1

    ROLES = (
        (ADVISER, 'Рекламодатель'),
        (SITE_OWNER, 'Владелец сайта')
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ['email']

    email = models.EmailField(verbose_name='Email', unique=True)
    first_name = models.CharField(verbose_name='Имя', max_length=128, null=True, blank=True)
    last_name = models.CharField(verbose_name='Фамилия', max_length=128, null=True, blank=True)
    role = models.PositiveIntegerField(verbose_name='Роль', choices=ROLES, null=True, blank=True)

    is_active = models.BooleanField(verbose_name='Активен?', default=False)
    is_staff = models.BooleanField(verbose_name='Персонал?', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        parts = []
        if self.first_name:
            parts.append(self.first_name.capitalize())
        if self.last_name:
            parts.append(self.last_name.capitalize())
        return ' '.join(parts)

    def get_human_role(self):
        if self.role is not None:
            return dict(self.ROLES).get(self.role)
        return 'Роль неизвестна'

    def get_short_name(self):
        return self.email


class ACompany(DefaultModel):
    class Meta:
        verbose_name = 'Рекламная кампания'
        verbose_name_plural = 'рекламные кампании'
        ordering = ['-created']

    title = models.CharField(verbose_name='Название продукта', max_length=100)
    text = models.TextField(verbose_name='Текст', max_length=300)
    owner = models.ForeignKey('User', verbose_name='Владелец')
    link = models.URLField(max_length=256, verbose_name='Ссылка перехода', blank=True, null=True)
    max_score = models.PositiveIntegerField(verbose_name='Макс. траты в неделю', blank=True, null=True)

    def __str__(self):
        return self.title

    def as_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'text': self.text,
            'link': self.link,
            'max_score': self.max_score,
            'owner_id': self.owner.id,
            'details_url': reverse('core:company_details', args=[self.id]),
        }


class ImageAttachment(DefaultModel):
    class Meta:
        verbose_name = 'Картинка'
        verbose_name_plural = 'картинки'
        ordering = ['-weight']

    company = models.ForeignKey('ACompany', verbose_name='Рекламная компания')
    image = models.ImageField(verbose_name='Файл картинки', upload_to='images')
    weight = models.IntegerField(verbose_name='Вес картинки', default=1)

    def __str__(self):
        return '{} Image {}'.format(self.company, self.id)


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

    title = models.CharField(verbose_name='Название сайта', max_length=100)
    topic = models.PositiveIntegerField(verbose_name='Тип площадки', choices=TOPICS)
    link = models.URLField(max_length=256, verbose_name='Домен сайта')
    owner = models.ForeignKey('User', verbose_name='Владелец')

    def __str__(self):
        return self.title

    def get_human_topic(self):
        if self.topic is not None and self.topic in self.TOPICS:
            return dict(self.TOPICS).get(self.topic)
        return 'Тип неизвестен'

    def as_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'topic': self.get_human_topic(),
            'link': self.link,
            'owner_id': self.owner.id,
            'details_url': reverse('core:site_details', args=[self.id]),
        }
