from django.contrib import admin
from .models import CompanySelection

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
