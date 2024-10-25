from django.db import models
from resumes.models import Resume
from companies.models import Interviewer


class CompanySelection(models.Model):
    selection_status_choices = [
        ('На рассмотрении', 'На рассмотрении'),
        ('Принят', 'Принят'),
        ('Отклонен', 'Отклонен')
    ]

    interviewer = models.ForeignKey(Interviewer, on_delete=models.CASCADE, verbose_name='Интервьюер')
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, verbose_name='Резюме')
    status = models.CharField(max_length=20, choices=selection_status_choices, verbose_name='Статус')

    def __str__(self):
        return f"{self.resume.candidate.user.email} - {self.status}"

    class Meta:
        verbose_name = 'Отбор компании'  # Название таблицы в единственном числе
        verbose_name_plural = 'Отборы компаний'  # Название таблицы во множественном числе


class TestTaskItem(models.Model):
    test_task = models.ForeignKey('tasks.TestTask', on_delete=models.CASCADE, verbose_name='Тестовое задание')
    task_item = models.ForeignKey('tasks.TaskItem', on_delete=models.CASCADE, verbose_name='Элемент задания')
    candidate_answer = models.TextField(verbose_name='Ответ кандидата')
    interviewer_comment = models.TextField(null=True, blank=True, verbose_name='Комментарий интервьюера')

    def __str__(self):
        return f"Элемент задания: {self.task_item} - Тестовое задание: {self.test_task}"

    class Meta:
        verbose_name = 'Элемент задания теста'  # Название таблицы в единственном числе
        verbose_name_plural = 'Элементы задания теста'  # Название таблицы во множественном числе
