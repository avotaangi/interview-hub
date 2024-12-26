from django.db import models
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from simple_history.models import HistoricalRecords
from users.models import Candidate


class Skill(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название навыка")
    description = models.TextField(
        null=True, blank=True, verbose_name="Описание навыка"
    )
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"

    # Валидация на уровне модели
    def clean(self):
        if len(self.name) < 2:
            raise ValidationError(
                {"name": "Название навыка должно быть не менее 2 символов."}
            )


class JobExperience(models.Model):
    company = models.CharField(max_length=255, verbose_name="Компания")
    position = models.CharField(max_length=255, verbose_name="Должность")
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(null=True, blank=True, verbose_name="Дата окончания")
    responsibilities = models.TextField(verbose_name="Обязанности")
    candidate = models.ForeignKey(
        Candidate, on_delete=models.CASCADE, verbose_name="Кандидат"
    )
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.position} в {self.company}"

    class Meta:
        verbose_name = "Опыт работы"
        verbose_name_plural = "Опыт работы"

    # Валидация на уровне модели
    def clean(self):
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError(
                {"end_date": "Дата окончания не может быть раньше даты начала."}
            )


class ResumeSkill(models.Model):
    resume = models.ForeignKey(
        "Resume", on_delete=models.CASCADE, verbose_name="Резюме"
    )
    skill = models.ForeignKey(
        "Skill", on_delete=models.CASCADE, verbose_name="Навык"
    )
    proficiency_level = models.CharField(
        max_length=50, verbose_name="Уровень владения"
    )
    added_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата добавления"
    )

    class Meta:
        verbose_name = "Навык резюме"
        verbose_name_plural = "Навыки резюме"


class Resume(models.Model):
    candidate = models.ForeignKey(
        Candidate, on_delete=models.CASCADE, verbose_name="Кандидат"
    )
    desired_position = models.CharField(
        max_length=255, verbose_name="Желаемая должность"
    )
    desired_salary = models.IntegerField(verbose_name="Желаемая зарплата")
    skills = models.ManyToManyField(
        Skill, through="ResumeSkill", related_name="resumes", verbose_name="Навыки"
    )
    job_experiences = models.ManyToManyField(
        JobExperience,
        related_name="job_experience",
        verbose_name="Опыт работы",
        blank=True,
    )
    additional_info = models.TextField(
        null=True, blank=True, verbose_name="Дополнительная информация"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.candidate.user.email} - {self.desired_position}"

    class Meta:
        verbose_name = "Резюме"
        verbose_name_plural = "Резюме"

    # Валидация на уровне модели
    def clean(self):
        if self.desired_salary is None or self.desired_salary <= 0:
            raise ValidationError(
                {"desired_salary": "Желаемая зарплата должна быть положительной."}
            )


# Универсальная связь с ContentTypes
class Note(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    note = models.TextField(verbose_name="Заметка")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Заметка"
        verbose_name_plural = "Заметки"
