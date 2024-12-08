from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export.formats.base_formats import XLSX, CSV, JSON
from .models import Interview, InterviewTaskItem
from .resources import InterviewResource, InterviewTaskItemResource


# Админка для Interview
@admin.register(Interview)
class InterviewAdmin(ImportExportModelAdmin):
    resource_class = InterviewResource

    # Форматы экспорта
    def get_export_formats(self):
        return [XLSX, CSV, JSON]

    def get_export_queryset(self, request):
        """
        Отбор интревью, имеющих статус 'На рассмотрении'"
        """
        queryset = super().get_export_queryset(request)
        # фильтруем только завершенные интервью
        return queryset.filter(status="Запланировано")

    list_display = (
        "selection",
        "start_time",
        "end_time",
        "status",
        "result",
        "short_feedback",
    )
    list_filter = ("status", "result", "start_time")
    search_fields = ("selection__resume__candidate__user__email", "status", "result")
    raw_id_fields = ("selection",)
    date_hierarchy = "start_time"
    list_display_links = ("selection", "start_time")

    @admin.display(description="Feedback")
    def short_feedback(self, obj):
        return obj.feedback[:50] if obj.feedback else "No feedback available"


# Админка для InterviewTaskItem
@admin.register(InterviewTaskItem)
class InterviewTaskItemAdmin(ImportExportModelAdmin):
    resource_class = InterviewTaskItemResource

    # Форматы экспорта
    def get_export_formats(self):
        return [XLSX, CSV, JSON]

    def get_export_queryset(self, request):
        """
        Метод для кастомизации выборки данных для задания интервью.
        Выбор только те задания, которые еще не были выполнены кандидатом.
        """
        queryset = super().get_export_queryset(request)
        # Пример: выбираем только те задания, которые не имеют ответа
        return queryset.filter(candidate_answer__isnull=False)

    list_display = ("interview", "task_item", "short_candidate_answer")
    list_filter = ("task_item",)
    search_fields = (
        "interview__selection__resume__candidate__user__email",
        "task_item__title",
    )
    raw_id_fields = ("interview", "task_item")
    readonly_fields = ("candidate_answer",)

    @admin.display(description="Candidate Answer")
    def short_candidate_answer(self, obj):
        return (
            obj.candidate_answer[:50] if obj.candidate_answer else "No answer provided"
        )
