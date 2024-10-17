from django.contrib import admin
from .models import Resume, Job

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'desired_position', 'desired_salary')
    search_fields = ('candidate__user__email', 'desired_position')

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('resume', 'company', 'position', 'start_date', 'end_date')
    search_fields = ('resume__candidate__user__email', 'company', 'position')


