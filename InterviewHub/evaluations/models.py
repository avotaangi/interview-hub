from django.db import models
from interviews.models import Interview
from tasks.models import TestTask

class InterviewEvaluation(models.Model):
    interview = models.OneToOneField(Interview, on_delete=models.CASCADE, verbose_name='Интервью')
    hard_skills_rate = models.IntegerField(verbose_name='Оценка хард скиллов')
    soft_skills_rate = models.IntegerField(verbose_name='Оценка софт скиллов')
    final_feedback = models.TextField(verbose_name='Финальная обратная связь')
    overall_result = models.CharField(max_length=20, choices=[('Принято', 'Принято'), ('Отклонено', 'Отклонено')], verbose_name='Общий результат')
    evaluation_date = models.DateField(auto_now_add=True, verbose_name='Дата оценки')

    class Meta:
        verbose_name = 'Оценка интервью'  # Название таблицы в единственном числе
        verbose_name_plural = 'Оценки интервью'  # Название таблицы во множественном числе


class TestEvaluation(models.Model):
    test_task = models.OneToOneField(TestTask, on_delete=models.CASCADE, verbose_name='Тестовое задание')
    result = models.CharField(max_length=20, choices=[('Принято', 'Принято'), ('Отклонено', 'Отклонено')], verbose_name='Результат')
    feedback = models.TextField(verbose_name='Обратная связь')
    evaluation_date = models.DateField(auto_now_add=True, verbose_name='Дата оценки')

    class Meta:
        verbose_name = 'Оценка теста'  # Название таблицы в единственном числе
        verbose_name_plural = 'Оценки тестов'  # Название таблицы во множественном числе
