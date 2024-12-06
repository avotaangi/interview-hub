from django.db import models
from simple_history.models import HistoricalRecords


class TestTask(models.Model):
    selection = models.ForeignKey(
        "selections.CompanySelection",
        on_delete=models.CASCADE,
        verbose_name="Отбор компании",
    )
    start_time = models.DateTimeField(verbose_name="Время начала")
    end_time = models.DateTimeField(verbose_name="Время окончания")
    duration = models.IntegerField(verbose_name="Продолжительность (мин)")

    result_choices = [("Принято", "Принято"), ("Отклонено", "Отклонено")]
    result = models.CharField(
        null=True,
        blank=True,
        max_length=20,
        choices=result_choices,
        verbose_name="Результат",
    )
    recording_url = models.URLField(null=True, blank=True, verbose_name="URL записи")
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Тестовое задание"  # Название таблицы в единственном числе
        verbose_name_plural = (
            "Тестовые задания"  # Название таблицы во множественном числе
        )

    def __str__(self):
        return f"{self.selection.resume.candidate.user.email} - {self.start_time.strftime('%d.%m.%Y %H:%M')}"


class TestTaskItem(models.Model):
    test_task = models.ForeignKey(
        "TestTask", on_delete=models.CASCADE, verbose_name="Тестовое задание"
    )
    task_item = models.ForeignKey(
        "tasks.TaskItem", on_delete=models.CASCADE, verbose_name="Элемент задания"
    )
    candidate_answer = models.TextField(verbose_name="Ответ кандидата")
    interviewer_comment = models.TextField(
        null=True, blank=True, verbose_name="Комментарий интервьюера"
    )
    history = HistoricalRecords()

    def __str__(self):
        return f"Элемент задания: {self.task_item} - Тестовое задание: {self.test_task}"

    class Meta:
        verbose_name = "Элемент задания к тестовому заданию"  # Название таблицы в единственном числе
        verbose_name_plural = "Элементы задания к тестовым заданиям"  # Название таблицы во множественном числе
