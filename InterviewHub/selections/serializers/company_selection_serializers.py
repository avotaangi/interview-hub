from rest_framework import serializers
from ..models import CompanySelection
from resumes.models import Resume
from users.models import Interviewer


class CompanySelectionSerializer(serializers.ModelSerializer):
    # Сериализация связанных объектов для читабельности
    interviewer_email = serializers.EmailField(source='interviewer.user.email', read_only=True)
    resume_candidate_email = serializers.EmailField(source='resume.candidate.user.email', read_only=True)

    # Добавляем поля для получения interviewer's id и resume's id
    interviewer_id = serializers.PrimaryKeyRelatedField(queryset=Interviewer.objects.all(), source='interviewer', write_only=True)
    resume_id = serializers.PrimaryKeyRelatedField(queryset=Resume.objects.all(), source='resume', write_only=True)

    class Meta:
        model = CompanySelection
        fields = [
            'id',
            'interviewer',
            'resume',
            'status',
            'interviewer_email',
            'resume_candidate_email',
            'interviewer_id',  # Добавляем поля для id
            'resume_id'  # Добавляем поля для id
        ]
        read_only_fields = ['interviewer_email', 'resume_candidate_email']
        depth = 3

    def create(self, validated_data):
        # Убираем из validated_data поля, которые содержат вложенные объекты
        interviewer = validated_data.pop('interviewer', None)
        resume = validated_data.pop('resume', None)

        # Создаем объект CompanySelection
        company_selection = CompanySelection.objects.create(
            interviewer=interviewer,
            resume=resume,
            **validated_data
        )

        return company_selection

    def update(self, instance, validated_data):
        # Обновляем только поля, которые были переданы в validated_data
        interviewer = validated_data.pop('interviewer', None)
        resume = validated_data.pop('resume', None)

        # Обновляем поля объекта CompanySelection
        if interviewer:
            instance.interviewer = interviewer
        if resume:
            instance.resume = resume

        instance.status = validated_data.get('status', instance.status)
        instance.save()

        return instance
