from datetime import datetime

from django.utils.timezone import is_aware, make_aware
from rest_framework import serializers
from ..models import Interview


class InterviewSerializer(serializers.ModelSerializer):
    selection_id = serializers.IntegerField(source='selection.id', read_only=True)

    class Meta:
        model = Interview
        fields = [
            'id', 'selection', 'selection_id', 'start_time', 'end_time', 'duration',
            'type', 'status', 'feedback', 'notes', 'hard_skills_rate',
            'soft_skills_rate', 'result', 'recording_url'
        ]

    def validate_start_time(self, value):
        """
        Проверка, что время начала интервью указано в будущем.
        """
        now = datetime.now()
        # Убедимся, что обе даты aware (с временной зоной)
        if not is_aware(value):
            value = make_aware(value)
        if not is_aware(now):
            now = make_aware(now)

        if value < now:
            raise serializers.ValidationError("Время начала интервью должно быть в будущем.")
        return value

    def validate_hard_skills_rate(self, value):
        """
        Проверка оценки хард-скиллов (0-10).
        """
        if value is not None and (value < 0 or value > 10):
            raise serializers.ValidationError("Оценка хард-скиллов должна быть в диапазоне от 0 до 10.")
        return value

    def validate_soft_skills_rate(self, value):
        """
        Проверка оценки софт-скиллов (0-10).
        """
        if value is not None and (value < 0 or value > 10):
            raise serializers.ValidationError("Оценка софт-скиллов должна быть в диапазоне от 0 до 10.")
        return value

    def validate_status(self, value):
        """
        Проверка, что статус соответствует допустимым значениям.
        """
        valid_statuses = [choice[0] for choice in Interview.interview_status_choices]
        if value not in valid_statuses:
            raise serializers.ValidationError(f"Недопустимый статус. Доступные значения: {', '.join(valid_statuses)}.")
        return value

    def validate_result(self, value):
        """
        Проверка, что результат соответствует допустимым значениям.
        """
        valid_results = [choice[0] for choice in Interview.result_choices]
        if value and value not in valid_results:
            raise serializers.ValidationError(f"Недопустимый результат. Доступные значения: {', '.join(valid_results)}.")
        return value

    def validate_recording_url(self, value):
        """
        Проверка корректности URL записи (если указан).
        """
        if value and not value.startswith("http"):
            raise serializers.ValidationError("URL записи должен быть корректным и начинаться с http/https.")
        return value

    def validate(self, data):
        """
        Общая проверка: время начала должно быть меньше времени окончания.
        """
        start_time = data.get('start_time')
        end_time = data.get('end_time')

        if start_time and end_time and start_time >= end_time:
            raise serializers.ValidationError("Время начала должно быть меньше времени окончания.")
        return data
