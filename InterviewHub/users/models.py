from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone = models.CharField(max_length=20, null=True, blank=True)
    avatar_url = models.URLField(max_length=255, null=True, blank=True)
    gender_choices = [
        ('Мужской', 'Мужской'),
        ('Женский', 'Женский')
    ]
    gender = models.CharField(max_length=10, choices=gender_choices, null=True, blank=True)


class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    social_media = models.URLField(null=True, blank=True)
