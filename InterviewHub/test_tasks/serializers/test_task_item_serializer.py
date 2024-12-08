from rest_framework import serializers
from ..models import TestTaskItem


class TestTaskItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = TestTaskItem
        fields = [
            "id",
            "test_task",
            "task_item",
            "candidate_answer",
            "interviewer_comment",
        ]
