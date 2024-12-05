from import_export import resources, fields
from .models import TestTask, TestTaskItem


# Ресурс для TestTask
class TestTaskResource(resources.ModelResource):
    # Кастомное поле для отображения email кандидата
    candidate_email = fields.Field(column_name='Candidate Email')

    class Meta:
        model = TestTask
        fields = ('id', 'candidate_email', 'selection', 'start_time', 'end_time', 'result', 'duration')
        export_order = ('id', 'candidate_email', 'selection', 'start_time', 'end_time', 'result', 'duration')

    def get_candidate_email(self, obj):
        # Получаем email кандидата через связанную модель
        return obj.selection.resume.candidate.user.email

    def dehydrate_result(self, obj):
        # Преобразуем значение result в его отображаемое значение
        return obj.get_result_display()

    def get_export_queryset(self, queryset, *args, **kwargs):
        # Ограничиваем экспорт только записями с результатом "Принято"
        return queryset.filter(result='Принято')


# Ресурс для TestTaskItem
class TestTaskItemResource(resources.ModelResource):
    # Кастомные поля
    candidate_email = fields.Field(column_name='Candidate Email')
    task_title = fields.Field(column_name='Task Title')

    class Meta:
        model = TestTaskItem
        fields = ('id', 'candidate_email', 'test_task', 'task_title', 'candidate_answer', 'interviewer_comment')
        export_order = ('id', 'candidate_email', 'test_task', 'task_title', 'candidate_answer', 'interviewer_comment')

    def get_candidate_email(self, obj):
        # Получаем email кандидата через связанную модель TestTask
        return obj.test_task.selection.resume.candidate.user.email

    def get_task_title(self, obj):
        # Получаем название задания через task_item
        return obj.task_item.title

    def dehydrate_candidate_answer(self, obj):
        # Укорачиваем длинный ответ кандидата
        return (obj.candidate_answer[:100] + '...') if len(obj.candidate_answer) > 100 else obj.candidate_answer

    def get_export_queryset(self, queryset, *args, **kwargs):
        # Ограничиваем экспорт элементами, связанными с "Принято"
        return queryset.filter(test_task__result='Принято')
