from rest_framework import serializers
from .models import Skill, Resume, JobExperience

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

    # Валидация на уровне поля
    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError('Название навыка должно быть не менее 2 символов.')
        return value


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = '__all__'

    # Валидация на уровне поля
    def validate_desired_salary(self, value):
        if value <= 0:
            raise serializers.ValidationError('Желаемая зарплата должна быть положительной.')
        return value

    # Валидация на уровне объекта
    def validate(self, data):
        if not data.get('skills'):
            raise serializers.ValidationError('Необходимо указать хотя бы один навык.')
        return data


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobExperience
        fields = '__all__'

    # Валидация на уровне объекта
    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        if end_date and start_date and end_date < start_date:
            raise serializers.ValidationError({'end_date': 'Дата окончания не может быть раньше даты начала.'})
        return data
