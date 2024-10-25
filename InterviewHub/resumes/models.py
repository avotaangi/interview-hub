from django.db import models
from users.models import Candidate

class Skill(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название навыка')
    description = models.TextField(null=True, blank=True, verbose_name='Описание навыка')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Навык'  # Название таблицы в единственном числе
        verbose_name_plural = 'Навыки'  # Название таблицы во множественном числе


class Resume(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, verbose_name='Кандидат')
    desired_position = models.CharField(max_length=255, verbose_name='Желаемая должность')
    desired_salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Желаемая зарплата')
    skills = models.ManyToManyField(Skill, related_name='resumes', verbose_name='Навыки')  # Связь ManyToMany с моделью Skill
    additional_info = models.TextField(null=True, blank=True, verbose_name='Дополнительная информация')

    def __str__(self):
        return f"{self.candidate.user.email} - {self.desired_position}"

    class Meta:
        verbose_name = 'Резюме'  # Название таблицы в единственном числе
        verbose_name_plural = 'Резюме'  # Название таблицы во множественном числе


class Job(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, verbose_name='Резюме')
    company = models.CharField(max_length=255, verbose_name='Компания')
    position = models.CharField(max_length=255, verbose_name='Должность')
    start_date = models.DateField(verbose_name='Дата начала')
    end_date = models.DateField(null=True, blank=True, verbose_name='Дата окончания')
    responsibilities = models.TextField(verbose_name='Обязанности')

    def __str__(self):
        return f"{self.position} в {self.company}"

    class Meta:
        verbose_name = 'Работа'  # Название таблицы в единственном числе
        verbose_name_plural = 'Работы'  # Название таблицы во множественном числе
