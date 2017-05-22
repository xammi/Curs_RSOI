# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-22 07:04
from __future__ import unicode_literals

import core.models
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('first_name', models.CharField(blank=True, max_length=128, null=True, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, max_length=128, null=True, verbose_name='Фамилия')),
                ('role', models.PositiveIntegerField(blank=True, choices=[(0, 'Рекламодатель'), (1, 'Владелец сайта')], null=True, verbose_name='Роль')),
                ('is_active', models.BooleanField(default=False, verbose_name='Активен?')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Персонал?')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'пользователи',
                'ordering': ['email'],
            },
            managers=[
                ('objects', core.models.UserManager()),
            ],
        ),
    ]
