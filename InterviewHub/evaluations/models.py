from django.db import models
from interviews.models import Interview
from tasks.models import TestTask

class InterviewEvaluation(models.Model):
    interview = models.OneToOneField(Interview, on_delete=models.CASCADE)
    hard_skills_rate = models.IntegerField()
    soft_skills_rate = models.IntegerField()
    final_feedback = models.TextField()
    overall_result = models.CharField(max_length=20, choices=[('Принято', 'Принято'), ('Отклонено', 'Отклонено')])

class TestEvaluation(models.Model):
    test_task = models.OneToOneField(TestTask, on_delete=models.CASCADE)
    result = models.CharField(max_length=20, choices=[('Принято', 'Принято'), ('Отклонено', 'Отклонено')])
    feedback = models.TextField()
