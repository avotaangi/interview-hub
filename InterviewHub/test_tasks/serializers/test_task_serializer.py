from rest_framework import serializers
from ..models import TestTask


class TestTaskSerializer(serializers.ModelSerializer):
    selection_id = serializers.IntegerField(source='selection.id', read_only=True)

    class Meta:
        model = TestTask
        fields = [
            'id', 'selection_id', 'start_time', 'end_time', 'duration',
            'result', 'recording_url'
        ]

    def validate_start_time(self, value):
        """
        Проверка, что время начала тестового задания указано корректно.
        """
        from django.utils.timezone import now
        if value < now():
            raise serializers.ValidationError("Время начала тестового задания должно быть в будущем.")
        return value

    def validate_result(self, value):
        """
        Проверка, что результат соответствует допустимым значениям.
        """
        valid_results = [choice[0] for choice in TestTask.result_choices]
        if value and value not in valid_results:
            raise serializers.ValidationError(f"Недопустимый результат. Доступные значения: {', '.join(valid_results)}.")
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
