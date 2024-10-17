from django.db import models
from resumes.models import Resume
from companies.models import Interviewer


class CompanySelection(models.Model):
    selection_status_choices = [
        ('На рассмотрении', 'На рассмотрении'),
        ('Принят', 'Принят'),
        ('Отклонен', 'Отклонен')
    ]
    interviewer = models.ForeignKey(Interviewer, on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=selection_status_choices)


class TestTaskItem(models.Model):
    test_task = models.ForeignKey('tasks.TestTask', on_delete=models.CASCADE)
    task_item = models.ForeignKey('tasks.TaskItem', on_delete=models.CASCADE)
    candidate_answer = models.TextField()
    interviewer_comment = models.TextField(null=True, blank=True)
