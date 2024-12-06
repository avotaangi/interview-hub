from import_export import resources
from import_export.fields import Field
from .models import Interview, InterviewTaskItem


class InterviewResource(resources.ModelResource):
    # Пример кастомизации поля, для вывода статуса интервью в строковом формате
    status_display = Field(attribute='status', column_name='Статус',
                           widget=resources.widgets.ForeignKeyWidget(Interview, 'status'))

    class Meta:
        model = Interview
        fields = (
        'id', 'selection', 'start_time', 'end_time', 'duration', 'type', 'status_display', 'feedback', 'notes',
        'hard_skills_rate', 'soft_skills_rate', 'result', 'recording_url')
        export_order = (
        'id', 'selection', 'start_time', 'end_time', 'duration', 'type', 'status_display', 'feedback', 'notes',
        'hard_skills_rate', 'soft_skills_rate', 'result', 'recording_url')


    def dehydrate_status_display(self, interview):
        """
        Метод для кастомизации поля 'status' при экспорте.
        Это позволяет вернуть более читаемое значение для поля статуса.
        """
        return interview.get_status_display()

    def dehydrate_duration(self, interview):
        """
        Метод для кастомизации поля 'duration'. Например, форматировать продолжительность
        в виде 'X ч. Y мин.'
        """
        duration = interview.duration
        hours = duration // 60
        minutes = duration % 60
        return f"{hours} ч. {minutes} мин."


class InterviewTaskItemResource(resources.ModelResource):
    # Пример кастомизации поля, для вывода текста ответа кандидата
    candidate_answer_display = Field(attribute='candidate_answer', column_name='Ответ кандидата')

    class Meta:
        model = InterviewTaskItem
        fields = ('id', 'interview', 'task_item', 'candidate_answer_display')
        export_order = ('id', 'interview', 'task_item', 'candidate_answer_display')


    def dehydrate_candidate_answer_display(self, item):
        """
        Кастомизация поля 'candidate_answer' при экспорте.
        Может, например, обрабатывать длинные ответы и показывать их только частично.
        """
        answer = item.candidate_answer
        if len(answer) > 100:  # Ограничиваем длину ответа
            return answer[:100] + '...'
        return answer
