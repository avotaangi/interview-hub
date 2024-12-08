from rest_framework import serializers
from ..models import TaskItem
from .open_question_serializer import OpenQuestionSerializer
from .multiple_choice_question_serializer import MultipleChoiceQuestionSerializer
from .code_question_serializer import CodeQuestionSerializer


class TaskItemSerializer(serializers.ModelSerializer):
    open_questions = OpenQuestionSerializer(many=True, read_only=True)
    multiple_choice_questions = MultipleChoiceQuestionSerializer(
        many=True, read_only=True
    )
    code_questions = CodeQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = TaskItem
        fields = [
            "id",
            "title",
            "complexity",
            "task_condition",
            "open_questions",
            "multiple_choice_questions",
            "code_questions",
        ]

    def validate_complexity(self, value):
        """
        Validate that complexity is between 1 and 10.
        """
        if value < 1 or value > 10:
            raise serializers.ValidationError("Сложность должна быть от 1 до 10.")
        return value
