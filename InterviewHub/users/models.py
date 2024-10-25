from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='Телефон')
    avatar_url = models.URLField(max_length=255, null=True, blank=True, verbose_name='URL аватара')

    gender_choices = [
        ('Мужской', 'Мужской'),
        ('Женский', 'Женский')
    ]
    gender = models.CharField(max_length=10, choices=gender_choices, null=True, blank=True, verbose_name='Пол')

    def __str__(self):
        return self.email  # Добавляем метод __str__ для лучшего представления

    class Meta:
        verbose_name = 'Пользователь'  # Название таблицы в единственном числе
        verbose_name_plural = 'Пользователи'  # Название таблицы во множественном числе


class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    city = models.CharField(max_length=100, null=True, blank=True, verbose_name='Город')
    social_media = models.URLField(null=True, blank=True, verbose_name='Ссылка на социальные сети')

    def __str__(self):
        return self.user.email  # Добавляем метод __str__ для лучшего представления

    class Meta:
        verbose_name = 'Кандидат'  # Название таблицы в единственном числе
        verbose_name_plural = 'Кандидаты'  # Название таблицы во множественном числе
