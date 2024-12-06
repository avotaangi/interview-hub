from rest_framework import serializers
from ..models import Skill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

    # Валидация на уровне поля
    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError('Название навыка должно быть не менее 2 символов.')
        return value
