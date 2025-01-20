from datetime import datetime

from django.utils.timezone import is_aware, make_aware
from rest_framework import serializers
from ..models import Interview
from selections.models import CompanySelection


class InterviewSerializer(serializers.ModelSerializer):
    selection = serializers.PrimaryKeyRelatedField(queryset=CompanySelection.objects.all())

    class Meta:
        model = Interview
        fields = [
            "id",
            "selection",
            "start_time",
            "end_time",
            "duration",
            "type",
            "status",
            "feedback",
            "notes",
            "hard_skills_rate",
            "soft_skills_rate",
            "result",
            "recording_url",
            "additional_url",
        ]
