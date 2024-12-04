from rest_framework import serializers
from .models import CompanySelection

class CompanySelectionSerializer(serializers.ModelSerializer):
    # Сериализация связанных объектов для читабельности (опционально)
    interviewer_email = serializers.EmailField(source='interviewer.user.email', read_only=True)
    resume_candidate_email = serializers.EmailField(source='resume.candidate.user.email', read_only=True)

    class Meta:
        model = CompanySelection
        fields = [
            'id',
            'interviewer',
            'resume',
            'status',
            'interviewer_email',
            'resume_candidate_email'
        ]
        read_only_fields = ['interviewer_email', 'resume_candidate_email']

