from django.contrib import admin
from .models import TestTask, TestTaskItem


@admin.register(TestTask)
class TestTaskAdmin(admin.ModelAdmin):
    list_display = ('selection', 'start_time', 'end_time', 'result', 'duration')
    list_filter = ('result', 'selection__resume__candidate__user__email')  # Фильтр по результату и email кандидата
    search_fields = ('selection__resume__candidate__user__email', 'result')
    raw_id_fields = ('selection',)  # Используем raw_id_fields для ForeignKey
    date_hierarchy = 'start_time'  # Иерархия по дате начала


@admin.register(TestTaskItem)
class TestTaskItemAdmin(admin.ModelAdmin):
    list_display = ('test_task', 'task_item', 'candidate_answer', 'short_test_task')
    list_filter = ('test_task__selection__status',)  # Фильтрация по статусу выбора
    search_fields = ('test_task__selection__resume__candidate__user__email', 'task_item__title')
    raw_id_fields = ('test_task', 'task_item')  # Для ForeignKey
    readonly_fields = ('candidate_answer',)  # Поле для чтения
    list_display_links = ('test_task', 'task_item')  # Сделаем поля ссылками

    @admin.display(description='Test Task (short)')
    def short_test_task(self, obj):
        return f"{obj.test_task.selection.resume.candidate.user.email}"
