from django.contrib import admin
from .models import TaskItem, OpenQuestion, MultipleChoiceQuestion, CodeQuestion
from django.contrib.admin import SimpleListFilter


class TaskTypeFilter(SimpleListFilter):
    title = "Тип задания"
    parameter_name = "task_type"

    def lookups(self, request, model_admin):
        return [
            ("open_question", "С открытым ответом"),
            ("multiple_choice", "С выбором ответа"),
            ("code_question", "С написанием кода"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "open_question":
            return queryset.filter(openquestion__isnull=False)
        elif self.value() == "multiple_choice":
            return queryset.filter(multiplechoicequestion__isnull=False)
        elif self.value() == "code_question":
            return queryset.filter(codequestion__isnull=False)
        return queryset

class OpenQuestionInline(admin.StackedInline):
    model = OpenQuestion
    extra = 0
    verbose_name = "Задание с открытым ответом"
    verbose_name_plural = "Задания с открытым ответом"


class MultipleChoiceQuestionInline(admin.StackedInline):
    model = MultipleChoiceQuestion
    extra = 0
    verbose_name = "Задание с выбором ответа"
    verbose_name_plural = "Задания с выбором ответа"


class CodeQuestionInline(admin.StackedInline):
    model = CodeQuestion
    extra = 0
    verbose_name = "Задание с написанием кода"
    verbose_name_plural = "Задания с написанием кода"


@admin.register(TaskItem)
class TaskItemAdmin(admin.ModelAdmin):
    list_display = ("title", "complexity")
    search_fields = ("title",)
    list_filter = ("complexity",TaskTypeFilter)  # Фильтр по сложности
    list_display_links = ("title",)  # Сделаем "title" ссылкой

    # Добавление inline
    inlines = [OpenQuestionInline, MultipleChoiceQuestionInline, CodeQuestionInline]

@admin.register(OpenQuestion)
class OpenQuestionAdmin(admin.ModelAdmin):
    list_display = ("task_item", "correct_answer")
    search_fields = ("task_item__title",)


@admin.register(MultipleChoiceQuestion)
class MultipleChoiceQuestionAdmin(admin.ModelAdmin):
    list_display = ("task_item", "answer_text", "is_correct_answer")
    list_filter = ("is_correct_answer",)  # Фильтр по правильности ответа
    search_fields = ("task_item__title", "answer_text")


@admin.register(CodeQuestion)
class CodeQuestionAdmin(admin.ModelAdmin):
    list_display = ("task_item", "is_code_run", "input_data", "output_data")
    list_filter = ("is_code_run",)  # Фильтр по выполнению кода
    search_fields = ("task_item__title", "input_data", "output_data")
    list_display_links = ("task_item",)  # Сделаем "task_item" ссылкой
