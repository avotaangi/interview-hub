from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export.formats.base_formats import XLSX, CSV, JSON
from .models import TestTask, TestTaskItem
from .resources import TestTaskResource, TestTaskItemResource


@admin.register(TestTask)
class TestTaskAdmin(ImportExportModelAdmin):
    resource_class = TestTaskResource

    # Используем классы форматов из `import_export.formats.base_formats`
    def get_export_formats(self):
        return [XLSX, CSV, JSON]

    list_display = ("selection", "start_time", "end_time", "result", "duration")
    list_filter = (
        "result",
        "selection__resume__candidate__user__email",
    )  # Фильтр по результату и email клиента
    search_fields = ("selection__resume__candidate__user__email", "result")
    raw_id_fields = ("selection",)  # Используем raw_id_fields для ForeignKey
    date_hierarchy = "start_time"  # Иерархия по дате начала


@admin.register(TestTaskItem)
class TestTaskItemAdmin(ImportExportModelAdmin):
    resource_class = TestTaskItemResource

    # Используем классы форматов из `import_export.formats.base_formats`
    def get_export_formats(self):
        return [XLSX, CSV, JSON]

    list_display = ("test_task", "task_item", "candidate_answer", "short_test_task")
    list_filter = ("test_task__selection__status",)  # Фильтр по статусу отбора
    search_fields = (
        "test_task__selection__resume__candidate__user__email",
        "task_item__title",
    )
    raw_id_fields = ("test_task", "task_item")  # Для ForeignKey
    readonly_fields = ("candidate_answer",)  # Поле только для чтения
    list_display_links = ("test_task", "task_item")  # Делаем поля ссылками

    @admin.display(description="Test Task")
    def short_test_task(self, obj):
        # Отображаем email клиента
        return f"{obj.test_task.selection.resume.candidate.user.email}"
