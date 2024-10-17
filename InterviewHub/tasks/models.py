from django.db import models


class TaskItem(models.Model):
    title = models.CharField(max_length=255)
    complexity = models.IntegerField()
    task_condition = models.TextField()


class OpenQuestion(models.Model):
    task_item = models.ForeignKey(TaskItem, on_delete=models.CASCADE)
    correct_answer = models.TextField()


class MultipleChoiceQuestion(models.Model):
    task_item = models.ForeignKey(TaskItem, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=255)
    is_correct_answer = models.BooleanField()


class CodeQuestion(models.Model):
    task_item = models.ForeignKey(TaskItem, on_delete=models.CASCADE)
    language = models.CharField(max_length=255)
    is_code_run = models.BooleanField(default=False)
    code_snippet = models.TextField()


class TestTask(models.Model):
    selection = models.ForeignKey('selections.CompanySelection', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.IntegerField()
    result_choices = [
        ('Принято', 'Принято'),
        ('Отклонено', 'Отклонено')
    ]
    result = models.CharField(max_length=20, choices=result_choices)
    recording_url = models.URLField(null=True, blank=True)
