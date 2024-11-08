from django.contrib import admin
from .models import Resume, Job, Skill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'desired_position', 'desired_salary', 'short_skills')
    list_filter = ('desired_position', 'desired_salary')  # Фильтрация по позиции и зарплате
    search_fields = ('candidate__user__email', 'desired_position')
    raw_id_fields = ('candidate',)  # Используем raw_id_fields для ForeignKey
    list_display_links = ('candidate', 'desired_position')  # Связываем с ссылками
    filter_horizontal = ('skills',)  # Применяем filter_horizontal для ManyToMany поля skills

    @admin.display(description='Skills (short)')
    def short_skills(self, obj):
        return ', '.join(
            [skill.name for skill in obj.skills.all()[:3]]) if obj.skills.exists() else 'No skills provided'

    short_skills.short_description = 'Skills (short)'


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('resume', 'company', 'position', 'start_date', 'end_date', 'short_responsibilities')
    list_filter = ('company', 'position', 'start_date')  # Фильтрация по компании, позиции и дате начала
    search_fields = ('resume__candidate__user__email', 'company', 'position')
    raw_id_fields = ('resume',)  # Для ForeignKey
    date_hierarchy = 'start_date'  # Иерархия по дате начала работы

    @admin.display(description='Responsibilities (short)')
    def short_responsibilities(self, obj):
        return obj.responsibilities[:50] if obj.responsibilities else 'No responsibilities provided'

    short_responsibilities.short_description = 'Responsibilities (short)'
