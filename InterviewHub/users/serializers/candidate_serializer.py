from rest_framework import serializers
from .user_serializer import UserSerializer
from ..models import Candidate, User
from django.db import IntegrityError


class CandidateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # детальный вывод при GET
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )

    class Meta:
        model = Candidate
        fields = ["id", "user", "user_id", "birth_date", "city", "social_media"]

    def create(self, validated_data):
        user = validated_data.pop("user_id")

        # Проверка, существует ли уже кандидат с таким user_id
        existing_candidate = Candidate.objects.filter(user=user).first()
        if existing_candidate:
            raise serializers.ValidationError(
                {"user_id": "Пользователь уже связан с кандидатом."}
            )

        # Если кандидата нет, создаем нового
        return Candidate.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        user = validated_data.pop("user_id", None)  # Извлекаем user_id
        if user is not None:
            instance.user = user  # Обновляем связь с пользователем

        # Обновляем остальные поля
        instance.birth_date = validated_data.get("birth_date", instance.birth_date)
        instance.city = validated_data.get("city", instance.city)
        instance.social_media = validated_data.get(
            "social_media", instance.social_media
        )

        instance.save()
        return instance
