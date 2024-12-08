from rest_framework import serializers
from ..models import JobExperience


class JobExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobExperience
        fields = "__all__"

    # Валидация на уровне объекта
    def validate(self, data):
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        if end_date and start_date and end_date < start_date:
            raise serializers.ValidationError(
                {"end_date": "Дата окончания не может быть раньше даты начала."}
            )
        return data
