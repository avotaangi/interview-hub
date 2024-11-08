from django.db import models
from selections.models import CompanySelection
from tasks.models import TaskItem

class Interview(models.Model):
    interview_status_choices = [
        ('Запланировано', 'Запланировано'),
        ('Завершено', 'Завершено'),
        ('Отклонено', 'Отклонено')
    ]

    selection = models.ForeignKey(CompanySelection, on_delete=models.CASCADE, verbose_name='Отбор')
    start_time = models.DateTimeField(verbose_name='Время начала')
    end_time = models.DateTimeField(verbose_name='Время окончания')
    duration = models.IntegerField(verbose_name='Продолжительность (мин)', default=0)
    type = models.CharField(max_length=255, verbose_name='Тип интервью')
    status = models.CharField(choices=interview_status_choices, max_length=20, default='Запланировано', verbose_name='Статус')
    feedback = models.TextField(null=True, blank=True, verbose_name='Обратная связь')
    notes = models.TextField(null=True, blank=True, verbose_name='Примечания')
    hard_skills_rate = models.IntegerField(null=True, blank=True, verbose_name='Оценка хард скиллов')
    soft_skills_rate = models.IntegerField(null=True, blank=True, verbose_name='Оценка софт скиллов')

    result_choices = [
        ('Принято', 'Принято'),
        ('Отклонено', 'Отклонено')
    ]
    result = models.CharField(max_length=20, null=True, blank=True, choices=result_choices, verbose_name='Результат')
    recording_url = models.URLField(null=True, blank=True, verbose_name='URL записи')

    class Meta:
        verbose_name = 'Интервью'  # Название таблицы в единственном числе
        verbose_name_plural = 'Интервью'  # Название таблицы во множественном числе

    def save(self, *args, **kwargs):
        # Calculate the duration before saving
        if self.start_time and self.end_time:
            delta = self.end_time - self.start_time
            self.duration = int(delta.total_seconds() // 60)  # Convert seconds to minutes
        super().save(*args, **kwargs)


class InterviewTaskItem(models.Model):
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, verbose_name='Интервью')
    task_item = models.ForeignKey(TaskItem, on_delete=models.CASCADE, verbose_name='Задание')
    candidate_answer = models.TextField(verbose_name='Ответ кандидата')

    class Meta:
        verbose_name = 'Элемент задания к интервью'  # Название таблицы в единственном числе
        verbose_name_plural = 'Элементы задания к интервью'  # Название таблицы во множественном числе
