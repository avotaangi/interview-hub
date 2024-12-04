from drf_yasg import openapi
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.utils import timezone
from ..models import Resume, Skill, JobExperience
from ..serializers import ResumeSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ResumeViewSet(viewsets.ModelViewSet):
    """
    API для работы с резюме кандидатов.
    """
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['candidate', 'desired_position', 'desired_salary']
    search_fields = ['desired_position', 'additional_info']

    @swagger_auto_schema(
        operation_summary="Получить список резюме",
        operation_description="Получить список всех резюме с поддержкой фильтров, поиска и пагинации.",
        manual_parameters=[
            openapi.Parameter(name='candidate', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Уникальный ID кандидата'),
            openapi.Parameter(name='page', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Номер страницы'),
            openapi.Parameter(name='page_size', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Количество элементов на странице'),
            openapi.Parameter(name='search', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Поиск по желаемой должности или дополнительной информации'),
            openapi.Parameter(name='desired_position', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Фильтр по желаемой должности'),
            openapi.Parameter(name='desired_salary', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Фильтр по желаемой зарплате'),
        ],
        responses={200: ResumeSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Создать новое резюме",
        operation_description="Создать новое резюме для кандидата.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["candidate", "desired_position", "desired_salary"],
            properties={
                "candidate": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="ID кандидата, которому принадлежит резюме.",
                    example=1
                ),
                "desired_position": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Желаемая должность кандидата.",
                    example="Software Developer"
                ),
                "desired_salary": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Желаемая зарплата кандидата.",
                    example=60000
                ),
                "skills": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER),
                    description="Список ID навыков, которые кандидат хочет указать.",
                    example=[1, 2, 3]
                ),
                "job_experiences": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER),
                    description="Список ID опыта работы, который кандидат хочет указать.",
                    example=[5, 8]
                ),
                "additional_info": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Дополнительная информация о кандидате.",
                    example="Ищу удаленную работу, готов к переезду."
                )
            }
        ),
        responses={
            201: openapi.Response(
                description="Резюме успешно создано",
                examples={
                    "application/json": {
                        "id": 1,
                        "candidate": 1,
                        "desired_position": "Software Developer",
                        "desired_salary": 60000.00,
                        "skills": [1, 2, 3],
                        "job_experiences": [5, 8],
                        "additional_info": "Ищу удаленную работу, готов к переезду.",
                        "created_at": "2024-01-01T10:00:00Z"
                    }
                }
            ),
            400: "Ошибка валидации"
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Получить информацию о резюме",
        operation_description="Получить информацию о конкретном резюме по его ID.",
        responses={200: ResumeSerializer, 404: "Резюме не найдено"},
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее резюме"
            ),
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Обновить резюме",
        operation_description="Полностью обновить информацию о резюме.",
        request_body=ResumeSerializer,
        responses={200: ResumeSerializer, 400: "Ошибка валидации", 404: "Резюме не найдено"},
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее резюме"
            ),
        ]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Частично обновить резюме",
        operation_description="Частично обновить информацию о резюме.",
        request_body=ResumeSerializer,
        responses={200: ResumeSerializer, 400: "Ошибка валидации", 404: "Резюме не найдено"},
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее резюме"
            ),
        ]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Удалить резюме",
        operation_description="Удалить резюме по его ID.",
        responses={204: "Резюме успешно удалено", 404: "Резюме не найдено"},
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее резюме"
            ),
        ]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        method='get',
        operation_summary="Получить последние резюме",
        operation_description="Получить все резюме, созданные за последние 30 дней.",
        responses={200: ResumeSerializer(many=True)},
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее резюме"
            ),
        ]
    )
    @action(methods=['GET'], detail=False)
    def recent_resumes(self, request):
        recent_date = timezone.now() - timezone.timedelta(days=30)
        resumes = self.get_queryset().filter(created_at__gte=recent_date)
        page = self.paginate_queryset(resumes)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(resumes, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        method='post',
        operation_summary="Добавить навык к резюме",
        operation_description="Добавить навык к существующему резюме кандидата.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['skill_id'],
            properties={
                'skill_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    example=1,
                    description="ID навыка для добавления к резюме."
                ),
            }
        ),
        responses={
            200: "Навык добавлен",
            400: "Навык не найден"
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее резюме"
            ),
        ]
    )
    @action(methods=['POST'], detail=True)
    def add_skill(self, request, pk=None):
        resume = self.get_object()
        skill_id = request.data.get('skill_id')
        try:
            skill = Skill.objects.get(id=skill_id)
            resume.skills.add(skill)
            resume.save()
            return Response({'status': 'Навык добавлен'})
        except Skill.DoesNotExist:
            return Response({'error': 'Навык не найден'}, status=400)

    @swagger_auto_schema(
        method='post',
        operation_summary="Удалить навык из резюме",
        operation_description="Удалить навык из существующего резюме кандидата.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['skill_id'],
            properties={
                'skill_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    example=1,
                    description="ID навыка для удаления из резюме."
                ),
            }
        ),
        responses={
            200: "Навык удален",
            400: "Ошибка: Навык не найден или не связан с резюме"
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее резюме"
            ),
        ]
    )
    @action(methods=['POST'], detail=True)
    def remove_skill(self, request, pk=None):
        resume = self.get_object()
        skill_id = request.data.get('skill_id')
        try:
            skill = Skill.objects.get(id=skill_id)
            if skill in resume.skills.all():
                resume.skills.remove(skill)
                resume.save()
                return Response({'status': 'Навык удален'})
            else:
                return Response({'error': 'Навык не связан с данным резюме'}, status=400)
        except Skill.DoesNotExist:
            return Response({'error': 'Навык не найден'}, status=400)

    @swagger_auto_schema(
        operation_summary="Добавить опыт работы к резюме",
        operation_description="Добавить опыт работы к существующему резюме кандидата.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['job_experience_id'],
            properties={
                'job_experience_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    example=1,
                    description="ID опыта работы для добавления к резюме."
                ),
            }
        ),
        responses={
            200: "Опыт работы добавлен",
            400: "Ошибка: Опыт работы не найден"
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее резюме"
            ),
        ]
    )
    @action(methods=['POST'], detail=True)
    def add_job_experience(self, request, pk=None):
        resume = self.get_object()
        job_experience_id = request.data.get('job_experience_id')
        try:
            job_experience = JobExperience.objects.get(id=job_experience_id)
            resume.job_experiences.add(job_experience)
            resume.save()
            return Response({'status': 'Опыт работы добавлен'})
        except JobExperience.DoesNotExist:
            return Response({'error': 'Опыт работы не найден'}, status=400)

    @swagger_auto_schema(
        method='post',
        operation_summary="Удалить опыт работы из резюме",
        operation_description="Удалить опыт работы из существующего резюме кандидата.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['job_experience_id'],
            properties={
                'job_experience_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    example=1,
                    description="ID опыта работы для удаления из резюме."
                ),
            }
        ),
        responses={
            200: "Опыт работы удален",
            400: "Ошибка: Опыт работы не найден или не связан с резюме"
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее резюме"
            ),
        ]
    )
    @action(methods=['POST'], detail=True)
    def remove_job_experience(self, request, pk=None):
        resume = self.get_object()
        job_experience_id = request.data.get('job_experience_id')
        try:
            job_experience = JobExperience.objects.get(id=job_experience_id)
            if job_experience in resume.job_experiences.all():
                resume.job_experiences.remove(job_experience)
                resume.save()
                return Response({'status': 'Опыт работы удален'})
            else:
                return Response({'error': 'Опыт работы не связан с данным резюме'}, status=400)
        except JobExperience.DoesNotExist:
            return Response({'error': 'Опыт работы не найден'}, status=400)

