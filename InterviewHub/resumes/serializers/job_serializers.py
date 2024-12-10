from rest_framework import serializers
from ..models import JobExperience
from users.models import Candidate


class JobExperienceSerializer(serializers.ModelSerializer):
    candidate_id = serializers.PrimaryKeyRelatedField(
        queryset=Candidate.objects.all(), write_only=True
    )

    class Meta:
        model = JobExperience
        fields = "__all__"
        depth = 1

    # Валидация на уровне объекта
    def validate(self, data):
        start_date = data.get("start_date")
        end_date = data.get("end_date")

        # Проверка дат
        if end_date and start_date and end_date < start_date:
            raise serializers.ValidationError(
                {"end_date": "Дата окончания не может быть раньше даты начала."}
            )

        # Проверка наличия кандидата
        candidate = data.get("candidate_id")
        if not candidate:
            raise serializers.ValidationError({"candidate_id": "Кандидат не указан."})

        # Дополнительные проверки, если нужны
        return data

    def create(self, validated_data):
        candidate = validated_data.pop("candidate_id", None)

        # Убедимся, что кандидат существует
        if not Candidate.objects.filter(id=candidate.id).exists():
            raise serializers.ValidationError(
                {"candidate_id": "Указанный кандидат не существует."}
            )

        # Создаем объект JobExperience
        job_experience = JobExperience.objects.create(candidate=candidate, **validated_data)
        return job_experience

    def update(self, instance, validated_data):
        candidate = validated_data.pop("candidate_id", None)

        # Убедимся, что кандидат существует, если передан
        if candidate and not Candidate.objects.filter(id=candidate.id).exists():
            raise serializers.ValidationError(
                {"candidate_id": "Указанный кандидат не существует."}
            )

        # Обновляем поля объекта
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Обновляем связь с кандидатом, если указано
        if candidate:
            instance.candidate = candidate

        instance.save()
        return instance
