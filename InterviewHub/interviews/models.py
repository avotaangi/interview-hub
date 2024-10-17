from django.db import models
from selections.models import CompanySelection
from tasks.models import TaskItem

class Interview(models.Model):
    interview_status_choices = [
        ('Запланировано', 'Запланировано'),
        ('Завершено', 'Завершено'),
        ('Отклонено', 'Отклонено')
    ]
    selection = models.ForeignKey(CompanySelection, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.IntegerField()
    type = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=interview_status_choices)
    feedback = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    hard_skills_rate = models.IntegerField(null=True, blank=True)
    soft_skills_rate = models.IntegerField(null=True, blank=True)
    result_choices = [
        ('Принято', 'Принято'),
        ('Отклонено', 'Отклонено')
    ]
    result = models.CharField(max_length=20, choices=result_choices)
    recording_url = models.URLField(null=True, blank=True)

class InterviewTaskItem(models.Model):
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE)
    task_item = models.ForeignKey(TaskItem, on_delete=models.CASCADE)
    candidate_answer = models.TextField()
