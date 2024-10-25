from django.contrib import admin
from .models import Company, Interviewer


class InterviewerInline(admin.TabularInline):
    model = Interviewer
    extra = 1


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'established_date', 'display_interviewers')
    list_filter = ('location', 'established_date')
    search_fields = ('name', 'location')
    inlines = [InterviewerInline]
    date_hierarchy = 'established_date'

    @admin.display(description='Interviewers')
    def display_interviewers(self, obj):
        return ", ".join([interviewer.name for interviewer in obj.interviewer_set.all()])


@admin.register(Interviewer)
class InterviewerAdmin(admin.ModelAdmin):
    list_display = ('company__name', 'position', 'email', 'name')
    list_filter = ('company__name', 'position')
    search_fields = ('company__name', 'position', 'name', 'email')
    list_display_links = ('name', 'email')
    raw_id_fields = ('company',)
