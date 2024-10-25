from django.contrib import admin
from .models import User, Candidate

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
    readonly_fields = ('birth_date',)  # Поле для чтения (дата рождения)
    list_filter = ('city',)  # Фильтрация по городу
