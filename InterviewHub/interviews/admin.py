from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export.formats.base_formats import XLSX, CSV, JSON
from .models import Interview, InterviewTaskItem
from .resources import InterviewResource, InterviewTaskItemResource


# Админка для Interview
@admin.register(Interview)
class InterviewAdmin(ImportExportModelAdmin):
    resource_class = InterviewResource

    # Форматы экспорта
    def get_export_formats(self):
        return [XLSX, CSV, JSON]

    list_display = ('selection', 'start_time', 'end_time', 'status', 'result', 'short_feedback')
    list_filter = ('status', 'result', 'start_time')
    search_fields = ('selection__resume__candidate__user__email', 'status', 'result')
    raw_id_fields = ('selection',)
    date_hierarchy = 'start_time'
    list_display_links = ('selection', 'start_time')

    @admin.display(description='Feedback')
    def short_feedback(self, obj):
        return obj.feedback[:50] if obj.feedback else 'No feedback available'


# Админка для InterviewTaskItem
@admin.register(InterviewTaskItem)
class InterviewTaskItemAdmin(ImportExportModelAdmin):
    resource_class = InterviewTaskItemResource

    # Форматы экспорта
    def get_export_formats(self):
        return [XLSX, CSV, JSON]

    list_display = ('interview', 'task_item', 'short_candidate_answer')
    list_filter = ('task_item',)
    search_fields = ('interview__selection__resume__candidate__user__email', 'task_item__title')
    raw_id_fields = ('interview', 'task_item')
    readonly_fields = ('candidate_answer',)

    @admin.display(description='Candidate Answer')
    def short_candidate_answer(self, obj):
        return obj.candidate_answer[:50] if obj.candidate_answer else 'No answer provided'
