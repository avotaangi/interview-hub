from django.contrib import admin
from .models import Interview, InterviewTaskItem


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ('selection', 'start_time', 'end_time', 'status', 'result', 'short_feedback')
    list_filter = ('status', 'result', 'start_time')
    search_fields = ('selection__resume__candidate__user__email', 'status', 'result')
    raw_id_fields = ('selection',)  # Используем raw_id_fields для ForeignKey
    date_hierarchy = 'start_time'  # Сортировка по дате начала интервью
    list_display_links = ('selection', 'start_time')

    @admin.display(description='Feedback (short)')
    def short_feedback(self, obj):
        return obj.feedback[:50] if obj.feedback else 'No feedback available'

    short_feedback.short_description = 'Feedback (short)'


@admin.register(InterviewTaskItem)
class InterviewTaskItemAdmin(admin.ModelAdmin):
    list_display = ('interview', 'task_item', 'short_candidate_answer')
    list_filter = ('task_item',)
    search_fields = ('interview__selection__resume__candidate__user__email', 'task_item__title')
    raw_id_fields = ('interview', 'task_item')
    readonly_fields = ('candidate_answer',)

    @admin.display(description='Candidate Answer (short)')
    def short_candidate_answer(self, obj):
        return obj.candidate_answer[:50] if obj.candidate_answer else 'No answer provided'

    short_candidate_answer.short_description = 'Answer (short)'
