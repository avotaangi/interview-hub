from rest_framework import serializers
from ..models import Interview, InterviewTaskItem
from tasks.models import OpenQuestion, MultipleChoiceQuestion, CodeQuestion


class InterviewTaskItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewTaskItem
        fields = [
            'id', 'interview', 'task_item', 'candidate_answer'
        ]


class InterviewTaskItemDetailSerializer(serializers.ModelSerializer):
    interview = serializers.PrimaryKeyRelatedField(read_only=True)
    task = serializers.SerializerMethodField()
    correct_answers = serializers.SerializerMethodField()

    class Meta:
        model = InterviewTaskItem
        fields = ['id', 'interview', 'task', 'candidate_answer', 'correct_answers']

    def get_task(self, obj):
        """
        Формирует информацию о задаче.
        """
        task_item = obj.task_item  # Это объект модели TaskItem, связанный с InterviewTaskItem
        return {
            "task_id": task_item.id,
            "title": task_item.title,
            "complexity": task_item.complexity,
            "task_condition": task_item.task_condition,
        }

    def get_correct_answers(self, obj):
        """
        Извлекает правильные ответы для задачи.
        """
        task_item = obj.task_item  # Убедитесь, что вы работаете с task_item из InterviewTaskItem
        correct_answers = {
            "open_question": None,
            "multiple_choice": [],
            "code_question": None
        }

        # Извлечение правильных ответов для открытого вопроса
        open_question = OpenQuestion.objects.filter(task_item=task_item).first()
        if open_question:
            correct_answers["open_question"] = open_question.correct_answer

        # Извлечение правильных ответов для вопросов с выбором ответа
        multiple_choice_questions = MultipleChoiceQuestion.objects.filter(task_item=task_item, is_correct_answer=True)
        if multiple_choice_questions.exists():
            correct_answers["multiple_choice"] = [mc.answer_text for mc in multiple_choice_questions]

        # Извлечение правильных ответов для задания с написанием кода
        code_question = CodeQuestion.objects.filter(task_item=task_item).first()
        if code_question:
            correct_answers["code_question"] = {
                "language": code_question.language,
                "code_snippet": code_question.code_snippet
            }

        return correct_answers
