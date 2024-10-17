from django.contrib import admin
from .models import InterviewEvaluation, TestEvaluation

@admin.register(InterviewEvaluation)
class InterviewEvaluationAdmin(admin.ModelAdmin):
    list_display = ('interview', 'hard_skills_rate', 'soft_skills_rate', 'final_feedback', 'overall_result')
    search_fields = ('interview__selection__resume__candidate__user__email', 'overall_result')

@admin.register(TestEvaluation)
class TestEvaluationAdmin(admin.ModelAdmin):
    list_display = ('test_task', 'result', 'feedback')
    search_fields = ('test_task__selection__resume__candidate__user__email', 'result')


