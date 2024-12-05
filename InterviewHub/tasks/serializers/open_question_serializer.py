from rest_framework import serializers
from ..models import OpenQuestion

class OpenQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = OpenQuestion
        fields = ['id', 'task_item', 'correct_answer']
