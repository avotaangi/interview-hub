from django.contrib import admin
from .models import CompanySelection, TestTaskItem

@admin.register(CompanySelection)
class CompanySelectionAdmin(admin.ModelAdmin):
    list_display = ('interviewer', 'resume', 'status')
    search_fields = ('interviewer__company__company_name', 'resume__candidate__user__email', 'status')

@admin.register(TestTaskItem)
class TestTaskItemAdmin(admin.ModelAdmin):
    list_display = ('test_task', 'task_item', 'candidate_answer')
    search_fields = ('test_task__selection__resume__candidate__user__email', 'task_item__title')

