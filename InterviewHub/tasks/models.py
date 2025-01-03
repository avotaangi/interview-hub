from django.db import models
from simple_history.models import HistoricalRecords


# Кастомный QuerySet
class TaskItemQuerySet(models.QuerySet):
    def by_complexity(self, level):
        """Фильтрует задания по сложности."""
        return self.filter(complexity=level)

    def contains_keyword(self, keyword):
        """Ищет задания, содержащие ключевое слово в названии или условии."""
        return self.filter(models.Q(title__contains=keyword) | models.Q(task_condition__icontains=keyword))


# Кастомный менеджер
class TaskItemManager(models.Manager):
    def get_queryset(self):
        return TaskItemQuerySet(self.model, using=self._db)

    def by_complexity(self, level):
        return self.get_queryset().by_complexity(level)

    def contains_keyword(self, keyword):
        return self.get_queryset().contains_keyword(keyword)


class TaskItem(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название задания")
    complexity = models.IntegerField(verbose_name="Сложность")
    task_condition = models.TextField(verbose_name="Условие задания")
    image = models.ImageField(
        upload_to='task_images/',
        null=True,
        blank=True,
        verbose_name="Изображение задания"
    )
    history = HistoricalRecords()

    # Подключаем кастомный менеджер
    objects = TaskItemManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Элемент задания"
        verbose_name_plural = "Элементы задания"


class OpenQuestion(models.Model):
    task_item = models.ForeignKey(
        TaskItem, on_delete=models.CASCADE, verbose_name="Элемент задания"
    )
    correct_answer = models.TextField(verbose_name="Правильный ответ")
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Задание с открытым ответом"
        verbose_name_plural = "Задания с открытыми ответами"


class MultipleChoiceQuestion(models.Model):
    task_item = models.ForeignKey(
        TaskItem, on_delete=models.CASCADE, verbose_name="Элемент задания"
    )
    answer_text = models.CharField(max_length=255, verbose_name="Текст ответа")
    is_correct_answer = models.BooleanField(verbose_name="Правильный ответ")
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Задание с выбором ответа"
        verbose_name_plural = "Задания с выбором ответа"


class CodeQuestion(models.Model):
    task_item = models.ForeignKey(
        TaskItem, on_delete=models.CASCADE, verbose_name="Элемент задания"
    )
    is_code_run = models.BooleanField(default=False, verbose_name="Тест для примера")
    input_data = models.TextField(null=True, blank=True, verbose_name="Входные данные")
    output_data = models.TextField(null=True, blank=True, verbose_name="Выходные данные")
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Задание с написанием кода"
        verbose_name_plural = "Задания с написанием кода"
