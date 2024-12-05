from rest_framework import serializers
from .user_serializer import UserSerializer
from ..models import Interviewer, User, Company


class InterviewerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # детальный вывод при GET
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    company_id = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(), write_only=True)  # Изменили название на company_id

    class Meta:
        model = Interviewer
        fields = '__all__'
        depth = 1

    def create(self, validated_data):
        print(validated_data)
        user = validated_data.pop('user_id')
        company_id = validated_data.pop('company_id', None)

        # Проверка, существует ли уже кандидат с таким user_id
        existing_interviewer= Interviewer.objects.filter(user=user).first()
        if existing_interviewer:
            raise serializers.ValidationError({"user_id": "Пользователь уже является интервьюером."})

        if not company_id:
            raise serializers.ValidationError({"company_id": "Поле 'company_id' обязательно для заполнения."})

        # Если кандидата нет, создаем нового
        return Interviewer.objects.create(user=user, company=company_id, **validated_data)

    def update(self, instance, validated_data):
        user = validated_data.pop('user_id', None)  # Извлекаем user_id
        if user is not None:
            instance.user = user  # Обновляем связь с пользователем

        existing_interviewer = Interviewer.objects.filter(user=user).first()
        if existing_interviewer:
            raise serializers.ValidationError({"user_id": "Пользователь уже является интервьюером."})

        company_id = validated_data.pop('company_id', None)  # Переименовали в company_id
        if company_id is not None:
            instance.company_id = company_id  # Обновляем связь с компанией

        # Обновляем остальные поля
        instance.position = validated_data.get('position', instance.position)

        instance.save()
        return instance
