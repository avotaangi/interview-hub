from rest_framework import serializers
from ..models import MultipleChoiceQuestion

class MultipleChoiceQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = MultipleChoiceQuestion
        fields = ['id', 'task_item', 'answer_text', 'is_correct_answer']
