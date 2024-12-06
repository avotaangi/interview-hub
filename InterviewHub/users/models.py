from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone = models.CharField(
        max_length=20, null=True, blank=True, unique=True, verbose_name="Телефон"
    )
    avatar = models.ImageField(
        upload_to="user/avatar/",
        null=True,
        blank=True,
        verbose_name="Аватар пользователя",
    )
    gender_choices = [("Мужской", "Мужской"), ("Женский", "Женский")]
    gender = models.CharField(
        max_length=10, choices=gender_choices, null=True, blank=True, verbose_name="Пол"
    )

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Candidate(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    city = models.CharField(max_length=100, null=True, blank=True, verbose_name="Город")
    social_media = models.URLField(
        null=True, blank=True, verbose_name="Ссылка на социальные сети"
    )

    def __str__(self):
        return self.user.email  # Добавляем метод __str__ для лучшего представления

    class Meta:
        verbose_name = "Кандидат"  # Название таблицы в единственном числе
        verbose_name_plural = "Кандидаты"  # Название таблицы во множественном числе


class Company(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название компании")
    description = models.TextField(
        null=True, blank=True, verbose_name="Описание компании"
    )
    location = models.CharField(max_length=255, verbose_name="Местоположение")
    established_date = models.DateField(
        null=True, blank=True, verbose_name="Дата основания", default=timezone.now
    )
    logo = models.ImageField(
        upload_to="company_logos/",
        null=True,
        blank=True,
        verbose_name="Логотип компании",
    )  # New field

    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = "Компании"

    def __str__(self):
        return self.name


class Interviewer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, verbose_name="Компания"
    )
    position = models.CharField(max_length=255, verbose_name="Должность")

    class Meta:
        verbose_name = "Интервьюер"  # Название в единственном числе
        verbose_name_plural = "Интервьюеры"  # Название во множественном числе

    def __str__(self):
        return self.user.first_name
