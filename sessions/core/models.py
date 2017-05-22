import uuid

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models


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

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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

    def as_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'role': self.get_human_role(),
            'full_name': self.get_full_name(),
            'is_active': self.is_active,
            'is_staff': self.is_staff,
        }
