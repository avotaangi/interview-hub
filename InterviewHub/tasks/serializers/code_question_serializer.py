from rest_framework import serializers
from ..models import CodeQuestion


class CodeQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = CodeQuestion
        fields = [
            "id",
            "task_item",
            "is_code_run",
            "input_data",
            "output_data",
        ]
