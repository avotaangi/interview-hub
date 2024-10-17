from django.db import models

class Company(models.Model):
    company_name = models.CharField(max_length=255)
    company_description = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255)

class Interviewer(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    position = models.CharField(max_length=255)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
