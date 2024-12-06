from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models import Candidate
from ..serializers.candidate_serializer import CandidateSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class CandidateViewSet(viewsets.ModelViewSet):
    """
    API для управления кандидатами.
    """

    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["user__email", "city"]
    search_fields = ["user__email", "city", "social_media"]

    @swagger_auto_schema(
        operation_summary="Получить список кандидатов",
        operation_description="Получить список всех кандидатов с поддержкой фильтров, поиска и пагинации.",
        responses={
            200: openapi.Response(
                description="Успешное получение списка кандидатов",
                examples={
                    "application/json": {
                        "count": 1,
                        "next": None,
                        "previous": None,
                        "results": [
                            {
                                "id": 1,
                                "user": {
                                    "id": 1,
                                    "email": "example@example.com",
                                    "first_name": "Иван",
                                    "last_name": "Иванов",
                                },
                                "birth_date": "1990-01-01",
                                "city": "Москва",
                                "social_media": "https://vk.ru/profile",
                            }
                        ],
                    }
                },
            )
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Создать нового кандидата",
        operation_description="Создать запись нового кандидата с информацией о пользователе, дате рождения, городе и соцсетях.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["user", "city"],
            properties={
                "user_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    example=1,
                    description="ID пользователя, связанного с кандидатом.",
                ),
                "birth_date": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format="date",
                    example="1990-01-01",
                    description="Дата рождения кандидата в формате YYYY-MM-DD.",
                ),
                "city": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example="Москва",
                    description="Город проживания кандидата.",
                ),
                "social_media": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example="https://linkedin.com/in/example",
                    description="Ссылка на социальные сети кандидата.",
                ),
            },
        ),
        responses={
            201: openapi.Response(
                description="Кандидат успешно создан",
                examples={
                    "application/json": {
                        "id": 1,
                        "user": 1,
                        "birth_date": "1990-01-01",
                        "city": "Москва",
                        "social_media": "https://linkedin.com/in/example",
                    }
                },
            ),
            400: "Неверный запрос",
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Получить информацию о кандидате",
        operation_description="Получить информацию о конкретном кандидате по его ID.",
        responses={200: CandidateSerializer, 404: "Кандидат не найден"},
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее кандидата",
            ),
        ],
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Обновить информацию о кандидате",
        operation_description="Полностью обновить запись кандидата.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["user", "city"],
            properties={
                "user_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    example=1,
                    description="ID пользователя, связанного с кандидатом.",
                ),
                "birth_date": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format="date",
                    example="1990-01-01",
                    description="Дата рождения кандидата в формате YYYY-MM-DD.",
                ),
                "city": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example="Москва",
                    description="Город проживания кандидата.",
                ),
                "social_media": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example="https://linkedin.com/in/example",
                    description="Ссылка на социальные сети кандидата.",
                ),
            },
        ),
        responses={
            200: CandidateSerializer,
            400: "Неверный запрос",
            404: "Кандидат не найден",
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее кандидата",
            ),
        ],
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Частично обновить информацию о кандидате",
        operation_description="Частично обновить данные кандидата.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["user", "city"],
            properties={
                "user_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    example=1,
                    description="ID пользователя, связанного с кандидатом.",
                ),
                "birth_date": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format="date",
                    example="1990-01-01",
                    description="Дата рождения кандидата в формате YYYY-MM-DD.",
                ),
                "city": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example="Москва",
                    description="Город проживания кандидата.",
                ),
                "social_media": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example="https://linkedin.com/in/example",
                    description="Ссылка на социальные сети кандидата.",
                ),
            },
        ),
        responses={
            200: CandidateSerializer,
            400: "Неверный запрос",
            404: "Кандидат не найден",
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее кандидата",
            ),
        ],
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Удалить кандидата",
        operation_description="Удалить запись кандидата по его ID.",
        responses={204: "Кандидат успешно удален", 404: "Кандидат не найден"},
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее кандидата",
            ),
        ],
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
