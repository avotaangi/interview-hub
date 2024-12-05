from django.db import models
from resumes.models import Resume
from simple_history.models import HistoricalRecords
from users.models import Interviewer


class CompanySelection(models.Model):
    selection_status_choices = [
        ('На рассмотрении', 'На рассмотрении'),
        ('Принят', 'Принят'),
        ('Отклонен', 'Отклонен')
    ]

    interviewer = models.ForeignKey(Interviewer, on_delete=models.CASCADE, verbose_name='Интервьюер')
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, verbose_name='Резюме')
    status = models.CharField(max_length=20, choices=selection_status_choices, verbose_name='Статус')
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.resume.candidate.user.email} - {self.status}"

    class Meta:
        verbose_name = 'Отбор кандидатов'  # Название таблицы в единственном числе
        verbose_name_plural = 'Отборы кандидатов'  # Название таблицы во множественном числе

