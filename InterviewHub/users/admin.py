from django.contrib import admin
from .models import User, Candidate

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'gender', 'phone')
    search_fields = ('email', 'first_name', 'last_name')

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('user', 'birth_date', 'city', 'social_media')
    search_fields = ('user__email', 'city')

