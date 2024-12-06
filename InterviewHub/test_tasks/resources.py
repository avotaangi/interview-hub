import io

from import_export import resources, fields
from openpyxl.reader.excel import load_workbook
from openpyxl.styles import PatternFill

from .models import TestTask, TestTaskItem


class TestTaskResource(resources.ModelResource):
    candidate_email = fields.Field(column_name='Candidate Email', attribute='get_candidate_email')
    status = fields.Field(column_name='Status', readonly=True)

    class Meta:
        model = TestTask
        fields = ('id', 'candidate_email', 'selection', 'start_time', 'end_time', 'result', 'duration', 'status')
        export_order = ('id', 'candidate_email', 'selection', 'start_time', 'end_time', 'result', 'duration', 'status')

    def dehydrate_candidate_email(self, obj):
        return obj.selection.resume.candidate.user.email

    def dehydrate_result(self, obj):
        return obj.get_result_display()

    def dehydrate_status(self, obj):
        # На основе результата определяем статус
        if obj.get_result_display() == 'Принято':
            return 'Завершено успешно'
        elif obj.get_result_display() == 'Отклонено':
            return 'Завершено не успешно'
        else:
            return 'Не завершено'


class TestTaskItemResource(resources.ModelResource):
    candidate_email = fields.Field(column_name='Candidate Email', attribute='get_candidate_email')
    task_title = fields.Field(column_name='Task Title', attribute='get_task_title')

    class Meta:
        model = TestTaskItem
        fields = ('id', 'candidate_email', 'test_task', 'task_title', 'candidate_answer', 'interviewer_comment')
        export_order = ('id', 'candidate_email', 'test_task', 'task_title', 'candidate_answer', 'interviewer_comment')

    def dehydrate_candidate_email(self, obj):
        return obj.test_task.selection.resume.candidate.user.email

    def dehydrate_task_title(self, obj):
        return obj.task_item.title

    def dehydrate_candidate_answer(self, obj):
        return (obj.candidate_answer[:100] + '...') if len(obj.candidate_answer) > 100 else obj.candidate_answer
