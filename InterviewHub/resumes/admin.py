from .models import Resume, JobExperience, Skill
from django.contrib import admin
from .models import Resume, JobExperience, Skill
from django.contrib import admin
from django import forms

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
    )
    search_fields = ("candidate__user__email", "desired_position")
    raw_id_fields = ("candidate",)
    list_display_links = ("candidate", "desired_position")
    filter_horizontal = ("job_experiences",)
    readonly_fields = ("created_at",)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """
        Фильтрация Many-to-Many поля `job_experiences` на основе выбранного `candidate`.
        """
        if db_field.name == "job_experiences":
            # Если объект редактируется, фильтруем опыт работы по кандидату
            if request.resolver_match.args:
                resume_id = request.resolver_match.args[0]
                resume = Resume.objects.filter(pk=resume_id).first()
                if resume and resume.candidate:
                    kwargs["queryset"] = JobExperience.objects.filter(
                        candidate=resume.candidate
                    )
            # Если объект создается, поле изначально пусто
            elif "candidate" in request.POST:
                candidate_id = request.POST.get("candidate")
                kwargs["queryset"] = JobExperience.objects.filter(
                    candidate_id=candidate_id
                )
            else:
                kwargs["queryset"] = JobExperience.objects.none()
        return super().formfield_for_manytomany(db_field, request, **kwargs)

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

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(JobExperience)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        "company",
        "position",
        "start_date",
        "end_date",
        "short_responsibilities",
    )
    raw_id_fields = ("candidate",)
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
