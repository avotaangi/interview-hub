from django.db import models
from users.models import Candidate

class Resume(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    desired_position = models.CharField(max_length=255)
    desired_salary = models.DecimalField(max_digits=10, decimal_places=2)
    skills = models.TextField()
    additional_info = models.TextField(null=True, blank=True)

class Job(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    company = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    responsibilities = models.TextField()
