from django.db import models


class TaskItem(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название задания')
    complexity = models.IntegerField(verbose_name='Сложность')
    task_condition = models.TextField(verbose_name='Условие задания')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Элемент задания'  # Название таблицы в единственном числе
        verbose_name_plural = 'Элементы задания'  # Название таблицы во множественном числе


class OpenQuestion(models.Model):
    task_item = models.ForeignKey(TaskItem, on_delete=models.CASCADE, verbose_name='Элемент задания')
    correct_answer = models.TextField(verbose_name='Правильный ответ')

    class Meta:
        verbose_name = 'Открытый вопрос'  # Название таблицы в единственном числе
        verbose_name_plural = 'Открытые вопросы'  # Название таблицы во множественном числе


class MultipleChoiceQuestion(models.Model):
    task_item = models.ForeignKey(TaskItem, on_delete=models.CASCADE, verbose_name='Элемент задания')
    answer_text = models.CharField(max_length=255, verbose_name='Текст ответа')
    is_correct_answer = models.BooleanField(verbose_name='Правильный ответ')

    class Meta:
        verbose_name = 'Вопрос с выбором ответа'  # Название таблицы в единственном числе
        verbose_name_plural = 'Вопросы с выбором ответа'  # Название таблицы во множественном числе


class CodeQuestion(models.Model):
    task_item = models.ForeignKey(TaskItem, on_delete=models.CASCADE, verbose_name='Элемент задания')
    language = models.CharField(max_length=255, verbose_name='Язык программирования')
    is_code_run = models.BooleanField(default=False, verbose_name='Код выполнен')
    code_snippet = models.TextField(verbose_name='Код')

    class Meta:
        verbose_name = 'Кодовый вопрос'  # Название таблицы в единственном числе
        verbose_name_plural = 'Кодовые вопросы'  # Название таблицы во множественном числе


class TestTask(models.Model):
    selection = models.ForeignKey('selections.CompanySelection', on_delete=models.CASCADE,
                                  verbose_name='Отбор компании')
    start_time = models.DateTimeField(verbose_name='Время начала')
    end_time = models.DateTimeField(verbose_name='Время окончания')
    duration = models.IntegerField(verbose_name='Длительность')

    result_choices = [
        ('Принято', 'Принято'),
        ('Отклонено', 'Отклонено')
    ]
    result = models.CharField(max_length=20, choices=result_choices, verbose_name='Результат')
    recording_url = models.URLField(null=True, blank=True, verbose_name='URL записи')

    class Meta:
        verbose_name = 'Тестовое задание'  # Название таблицы в единственном числе
        verbose_name_plural = 'Тестовые задания'  # Название таблицы во множественном числе
