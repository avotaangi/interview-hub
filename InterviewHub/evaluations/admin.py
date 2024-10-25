from django.contrib import admin
from .models import InterviewEvaluation, TestEvaluation


@admin.register(InterviewEvaluation)
class InterviewEvaluationAdmin(admin.ModelAdmin):
    list_display = ('interview', 'hard_skills_rate', 'soft_skills_rate', 'overall_result', 'short_final_feedback')
    list_filter = ('overall_result', 'hard_skills_rate', 'soft_skills_rate')
    search_fields = ('interview__selection__resume__candidate__user__email', 'overall_result')
    raw_id_fields = ('interview',)
    readonly_fields = ('overall_result',)
    date_hierarchy = 'evaluation_date'

    @admin.display(description='Final Feedback')
    def short_final_feedback(self, obj):
        return obj.final_feedback[:50]

    short_final_feedback.short_description = 'Feedback (short)'


@admin.register(TestEvaluation)
class TestEvaluationAdmin(admin.ModelAdmin):
    list_display = ('test_task', 'result', 'short_feedback')
    list_filter = ('result',)
    search_fields = ('test_task__selection__resume__candidate__user__email', 'result')
    raw_id_fields = ('test_task',)
    readonly_fields = ('result',)
    date_hierarchy = 'evaluation_date'

    @admin.display(description='Feedback')
    def short_feedback(self, obj):
        return obj.feedback[:50]

    short_feedback.short_description = 'Feedback (short)'
