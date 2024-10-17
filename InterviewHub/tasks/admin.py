from django.contrib import admin
from .models import TestTask, TaskItem, OpenQuestion, MultipleChoiceQuestion, CodeQuestion

@admin.register(TestTask)
class TestTaskAdmin(admin.ModelAdmin):
    list_display = ('selection', 'start_time', 'end_time', 'result')
    search_fields = ('selection__resume__candidate__user__email', 'result')

@admin.register(TaskItem)
class TaskItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'complexity')
    search_fields = ('title',)

@admin.register(OpenQuestion)
class OpenQuestionAdmin(admin.ModelAdmin):
    list_display = ('task_item', 'correct_answer')
    search_fields = ('task_item__title',)

@admin.register(MultipleChoiceQuestion)
class MultipleChoiceQuestionAdmin(admin.ModelAdmin):
    list_display = ('task_item', 'answer_text', 'is_correct_answer')
    search_fields = ('task_item__title', 'answer_text')

@admin.register(CodeQuestion)
class CodeQuestionAdmin(admin.ModelAdmin):
    list_display = ('task_item', 'language', 'is_code_run')
    search_fields = ('task_item__title', 'language')


