from import_export import resources, fields
from .models import Interview, InterviewTaskItem


# Ресурс для Interview
class InterviewResource(resources.ModelResource):
    # Кастомные поля
    candidate_email = fields.Field(column_name='Candidate Email')

    class Meta:
        model = Interview
        fields = ('id', 'candidate_email', 'selection', 'start_time', 'end_time', 'status', 'result', 'feedback')
        export_order = ('id', 'candidate_email', 'selection', 'start_time', 'end_time', 'status', 'result', 'feedback')

    def get_candidate_email(self, obj):
        # Получаем email кандидата через связанную модель
        return obj.selection.resume.candidate.user.email

    def dehydrate_feedback(self, obj):
        # Укорачиваем поле feedback
        return obj.feedback[:100] if obj.feedback else 'No feedback available'


# Ресурс для InterviewTaskItem
class InterviewTaskItemResource(resources.ModelResource):
    # Кастомные поля
    candidate_email = fields.Field(column_name='Candidate Email')
    task_title = fields.Field(column_name='Task Title')

    class Meta:
        model = InterviewTaskItem
        fields = ('id', 'candidate_email', 'interview', 'task_title', 'candidate_answer')
        export_order = ('id', 'candidate_email', 'interview', 'task_title', 'candidate_answer')

    def get_candidate_email(self, obj):
        # Получаем email кандидата через связанную модель Interview
        return obj.interview.selection.resume.candidate.user.email

    def get_task_title(self, obj):
        # Получаем название задания
        return obj.task_item.title

    def dehydrate_candidate_answer(self, obj):
        # Укорачиваем ответ кандидата
        return obj.candidate_answer[:100] if obj.candidate_answer else 'No answer provided'
