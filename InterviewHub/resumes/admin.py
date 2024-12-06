from django.contrib import admin
from .models import Resume, JobExperience, Skill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


from django.contrib import admin
from .models import Resume


from django.contrib import admin


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для модели Resume.
    """

    list_display = (
        "candidate",
        "desired_position",
        "desired_salary",
        "short_skills",
        "short_job_experiences",
        "created_at",
    )
    list_filter = (
        "desired_position",
        "desired_salary",
    )  # Фильтрация по позиции и зарплате
    search_fields = ("candidate__user__email", "desired_position")
    raw_id_fields = ("candidate",)  # Используем raw_id_fields для ForeignKey
    list_display_links = ("candidate", "desired_position")  # Связываем с ссылками
    filter_horizontal = (
        "skills",
        "job_experiences",
    )  # Применяем filter_horizontal для ManyToMany полей
    readonly_fields = ("created_at",)  # Поле для отображения без возможности изменения

    @admin.display(description="Skills")
    def short_skills(self, obj):
        """
        Возвращает первые три навыка, связанных с резюме.
        """
        return (
            ", ".join([skill.name for skill in obj.skills.all()[:3]])
            if obj.skills.exists()
            else "No skills provided"
        )

    @admin.display(description="Job Experiences")
    def short_job_experiences(self, obj):
        """
        Возвращает первые три опыта работы, связанных с резюме.
        """
        return (
            ", ".join([job.company for job in obj.job_experiences.all()[:3]])
            if obj.job_experiences.exists()
            else "No experiences provided"
        )


@admin.register(JobExperience)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        "company",
        "position",
        "start_date",
        "end_date",
        "short_responsibilities",
    )
    list_filter = (
        "company",
        "position",
        "start_date",
    )  # Фильтрация по компании, позиции и дате начала
    search_fields = ("company", "position")
    date_hierarchy = "start_date"  # Иерархия по дате начала работы

    @admin.display(description="Responsibilities")
    def short_responsibilities(self, obj):
        return (
            obj.responsibilities[:50]
            if obj.responsibilities
            else "No responsibilities provided"
        )

    short_responsibilities.short_description = "Responsibilities"
