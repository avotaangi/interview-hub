from django.db import models
from django.utils import timezone

class Company(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название компании')
    description = models.TextField(null=True, blank=True, verbose_name='Описание компании')
    location = models.CharField(max_length=255, verbose_name='Местоположение')
    established_date = models.DateField(null=True, blank=True, verbose_name='Дата основания', default=timezone.now)

    class Meta:
        verbose_name = 'Компания'  # Название в единственном числе
        verbose_name_plural = 'Компании'  # Название во множественном числе

    def __str__(self):
        return self.name


class Interviewer(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Компания')
    position = models.CharField(max_length=255, verbose_name='Должность')
    name = models.CharField(max_length=100, verbose_name='ФИО')
    email = models.EmailField(max_length=100, verbose_name='Электронная почта')

    class Meta:
        verbose_name = 'Интервьюер'  # Название в единственном числе
        verbose_name_plural = 'Интервьюеры'  # Название во множественном числе

    def __str__(self):
        return self.name
