from django.contrib import admin
from .models import CompanySelection, TestTaskItem

@admin.register(CompanySelection)
class CompanySelectionAdmin(admin.ModelAdmin):
    list_display = ('interviewer', 'resume', 'status', 'short_resume', 'short_interviewer')
    list_filter = ('status', 'interviewer__company__name')  # Фильтрация по статусу и компании интервьюера
    search_fields = ('interviewer__company__name', 'resume__candidate__user__email', 'status')
    raw_id_fields = ('interviewer', 'resume')  # Используем raw_id_fields для ForeignKey
    list_display_links = ('interviewer', 'resume')  # Сделаем поля ссылками

    @admin.display(description='Resume (short)')
    def short_resume(self, obj):
        return obj.resume.candidate.user.email

    @admin.display(description='Interviewer (short)')
    def short_interviewer(self, obj):
        return obj.interviewer.name

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
