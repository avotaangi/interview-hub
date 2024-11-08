from django.contrib import admin
from django.utils.html import format_html

from .models import User, Candidate, Company, Interviewer

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'gender', 'phone')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('gender',)  # Фильтрация по полу
    readonly_fields = ('last_login',)  # Поле для чтения (последний вход)
    date_hierarchy = 'date_joined'  # Иерархия по дате регистрации

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('user', 'birth_date', 'city', 'social_media')
    search_fields = ('user__email', 'city')
    list_filter = ('city',)  # Фильтрация по городу


class InterviewerInline(admin.TabularInline):
    model = Interviewer
    extra = 1


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'established_date', 'display_interviewers', 'logo_preview')
    list_filter = ('location', 'established_date')
    search_fields = ('name', 'location')
    inlines = [InterviewerInline]
    date_hierarchy = 'established_date'

    @admin.display(description='Interviewers')
    def display_interviewers(self, obj):
        return ", ".join([interviewer.name for interviewer in obj.interviewer_set.all()])

    @admin.display(description='Логотип компании')
    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="50" height="50" />', obj.logo.url)
        return "-"


@admin.register(Interviewer)
class InterviewerAdmin(admin.ModelAdmin):
    list_display = ('company__name', 'position', 'email', 'name')
    list_filter = ('company__name', 'position')
    search_fields = ('company__name', 'position', 'name', 'email')
    list_display_links = ('name', 'email')
    raw_id_fields = ('company',)