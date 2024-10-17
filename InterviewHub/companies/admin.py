from django.contrib import admin
from .models import Company, Interviewer

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'location')
    search_fields = ('company_name', 'location')

@admin.register(Interviewer)
class InterviewerAdmin(admin.ModelAdmin):
    list_display = ('company', 'position', 'email')
    search_fields = ('company__company_name', 'position')

