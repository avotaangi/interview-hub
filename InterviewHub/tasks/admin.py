from django.contrib import admin
from .models import TestTask, TaskItem, OpenQuestion, MultipleChoiceQuestion, CodeQuestion

@admin.register(TestTask)
class TestTaskAdmin(admin.ModelAdmin):
    list_display = ('selection', 'start_time', 'end_time', 'result', 'duration')
    list_filter = ('result', 'selection__resume__candidate__user__email')  # Фильтр по результату и email кандидата
    search_fields = ('selection__resume__candidate__user__email', 'result')
    raw_id_fields = ('selection',)  # Используем raw_id_fields для ForeignKey
    date_hierarchy = 'start_time'  # Иерархия по дате начала
    readonly_fields = ('result',)  # Поле "result" только для чтения

@admin.register(TaskItem)
class TaskItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'complexity')
    search_fields = ('title',)
    list_filter = ('complexity',)  # Фильтр по сложности
    list_display_links = ('title',)  # Сделаем "title" ссылкой
    readonly_fields = ('complexity',)  # Сделаем "complexity" полем для чтения

@admin.register(OpenQuestion)
class OpenQuestionAdmin(admin.ModelAdmin):
    list_display = ('task_item', 'correct_answer')
    search_fields = ('task_item__title',)

@admin.register(MultipleChoiceQuestion)
class MultipleChoiceQuestionAdmin(admin.ModelAdmin):
    list_display = ('task_item', 'answer_text', 'is_correct_answer')
    list_filter = ('is_correct_answer',)  # Фильтр по правильности ответа
    search_fields = ('task_item__title', 'answer_text')

@admin.register(CodeQuestion)
class CodeQuestionAdmin(admin.ModelAdmin):
    list_display = ('task_item', 'language', 'is_code_run')
    list_filter = ('language', 'is_code_run')  # Фильтр по языку и выполнению кода
    search_fields = ('task_item__title', 'language')
    list_display_links = ('task_item', 'language')  # Сделаем "task_item" и "language" ссылками
