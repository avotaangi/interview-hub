from django.contrib import admin
from .models import Interview, InterviewTaskItem

@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ('selection', 'start_time', 'end_time', 'status', 'result')
    search_fields = ('selection__resume__candidate__user__email', 'status', 'result')

@admin.register(InterviewTaskItem)
class InterviewTaskItemAdmin(admin.ModelAdmin):
    list_display = ('interview', 'task_item', 'candidate_answer')
    search_fields = ('interview__selection__resume__candidate__user__email', 'task_item__title')

