from rest_framework import serializers
from ..models import CodeQuestion

class CodeQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = CodeQuestion
        fields = [
            'id',
            'task_item',
            'language',
            'is_code_run',
            'code_snippet',
        ]
