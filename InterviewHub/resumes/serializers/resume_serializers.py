from rest_framework import serializers

from .job_serializers import JobExperienceSerializer
from .skill_serializers import SkillSerializer
from ..models import Resume, Skill, JobExperience
from users.models import Candidate



class ResumeSerializer(serializers.ModelSerializer):
    candidate_id = serializers.PrimaryKeyRelatedField(
        queryset=Candidate.objects.all(), write_only=True
    )
    skills_data = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(), many=True, write_only=True
    )
    job_experiences_data = serializers.PrimaryKeyRelatedField(
        queryset=JobExperience.objects.all(), many=True, write_only=True
    )

    class Meta:
        model = Resume
        fields = "__all__"
        depth = 1

    # Валидация на уровне поля
    def validate_desired_salary(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Желаемая зарплата должна быть положительной."
            )
        return value

    # Валидация на уровне объекта
    def validate(self, data):
        # Получаем метод запроса
        request_method = self.context["request"].method

        # Если это POST-запрос, проверяем наличие навыков
        if request_method in ["POST", "PUT"]:
            if not data.get("skills_data", None):
                raise serializers.ValidationError(
                    "Необходимо указать хотя бы один навык."
                )

            # Проверка на наличие кандидата
            if not data.get("candidate_id"):
                raise serializers.ValidationError("Необходимо указать кандидата.")

        return data

    def create(self, validated_data):
        candidate = validated_data.pop("candidate_id", None)
        skills = validated_data.pop("skills_data", [])
        job_experiences = validated_data.pop("job_experiences_data", [])

        # Если кандидат не передан, берем текущего пользователя
        if not candidate:
            candidate = self.context["request"].user  # Текущий пользователь

        resume = Resume.objects.create(candidate=candidate, **validated_data)

        # Используем .set() для Many-to-Many полей
        resume.skills.set(skills)  # Устанавливаем связи с навыками
        resume.job_experiences.set(
            job_experiences
        )  # Устанавливаем связи с опытом работы

        return resume

    def update(self, instance, validated_data):
        candidate = validated_data.pop("candidate_id", None)
        if candidate:
            instance.candidate = candidate  # Обновляем связь с кандидатом
        skills = validated_data.pop("skills_data", None)
        job_experiences = validated_data.pop("job_experiences_data", None)

        # Обновление других полей
        instance.desired_position = validated_data.get(
            "desired_position", instance.desired_position
        )
        instance.desired_salary = validated_data.get(
            "desired_salary", instance.desired_salary
        )
        instance.additional_info = validated_data.get(
            "additional_info", instance.additional_info
        )

        # Используем .set() для обновления связей Many-to-Many
        if skills is not None:
            instance.skills.set(skills)
        if job_experiences is not None:
            instance.job_experiences.set(job_experiences)

        instance.save()

        return instance
