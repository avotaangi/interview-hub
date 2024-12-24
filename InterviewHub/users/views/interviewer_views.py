import logging

from django.core.cache import cache
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response

from ..models import Interviewer
from ..serializers.inteview_serializer import InterviewerSerializer

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..models import Interviewer
from ..serializers.inteview_serializer import InterviewerSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class InterviewerViewSet(viewsets.ModelViewSet):
    """
    API для управления интервьюерами.
    """

    queryset = Interviewer.objects.all()
    serializer_class = InterviewerSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter]
    search_fields = ["user__first_name", "user__email", "position"]

    @swagger_auto_schema(
        operation_summary="Получить список интервьюеров",
        operation_description="Получить список всех интервьюеров с поддержкой фильтров, поиска и пагинации.",
        manual_parameters=[
            openapi.Parameter(
                name="page",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Номер страницы для пагинации",
                default=1
            ),
            openapi.Parameter(
                name="page_size",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Количество элементов на странице",
                default=10
            ),
            openapi.Parameter(
                name="search",
                in_=openapi.IN_QUERY,
                description="Поиск по имени, email пользователя или должности.",
                type=openapi.TYPE_STRING,
            )
        ],
        responses={
            200: openapi.Response(
                description="Успешное получение списка интервьюеров",
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
                                    "name": "Иван Иванов",
                                    "email": "ivan@example.com",
                                },
                                "company": {"id": 2, "name": "Example Company"},
                                "position": "Senior Developer",
                            }
                        ],
                    }
                },
            )
        },
    )
    def list(self, request, *args, **kwargs):
        """
        Получить список интервьюеров с поддержкой кэширования.
        """
        # Генерация ключа для кэша на основе параметров запроса
        cache_key = f"interviewers_{request.query_params.urlencode()}"
        cached_data = cache.get(cache_key)

        if cached_data:
            # Возвращаем кэшированные данные
            return Response(cached_data, status=2)

        # Получаем данные через стандартный метод
        response = super().list(request, *args, **kwargs)

        # Сохраняем данные в кэш на 15 минут
        cache.set(cache_key, response.data, timeout=60 * 15)

        return response

    @swagger_auto_schema(
        operation_summary="Создать нового интервьюера",
        operation_description="Создать запись нового интервьюера с указанием пользователя, компании и должности.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["user_id", "company_id", "position"],
            properties={
                "user_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    example=1,
                    description="ID пользователя, связанного с интервьюером.",
                ),
                "company_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    example=2,
                    description="ID компании, в которой работает интервьюер.",
                ),
                "position": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example="Senior Developer",
                    description="Должность интервьюера.",
                ),
            },
        ),
        responses={
            201: openapi.Response(
                description="Интервьюер успешно создан",
                examples={
                    "application/json": {
                        "id": 1,
                        "user": {
                            "id": 1,
                            "name": "Иван Иванов",
                            "email": "ivan@example.com",
                        },
                        "company": {"id": 2, "name": "Example Company"},
                        "position": "Senior Developer",
                    }
                },
            ),
            400: "Неверный запрос",
        },
    )
    def create(self, request, *args, **kwargs):
        """
        Создать интервьюера и очистить кэш списка.
        """
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            cache.delete_pattern("interviewers_*")
        return response

    @swagger_auto_schema(
        operation_summary="Получить информацию об интервьюере",
        operation_description="Получить информацию о конкретном интервьюере по его ID.",
        responses={200: InterviewerSerializer, 404: "Интервьюер не найден"},
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее интервьюера",
            ),
        ],
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Получить информацию об интервьюере с поддержкой кэширования.
        """
        instance_id = kwargs.get("pk")
        cache_key = f"interviewer_{instance_id}"

        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        response = super().retrieve(request, *args, **kwargs)
        if response.status_code == 200:
            cache.set(cache_key, response.data, timeout=60 * 15)
        return response

    @swagger_auto_schema(
        operation_summary="Обновить информацию об интервьюере",
        operation_description="Полностью обновить запись интервьюера.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["user_id", "company_id", "position"],
            properties={
                "user_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    example=1,
                    description="ID пользователя, связанного с интервьюером.",
                ),
                "company_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    example=2,
                    description="ID компании, в которой работает интервьюер.",
                ),
                "position": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example="Senior Developer",
                    description="Должность интервьюера.",
                ),
            },
        ),
        responses={
            200: InterviewerSerializer,
            400: "Неверный запрос",
            404: "Интервьюер не найден",
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее интервьюера",
            ),
        ],
    )
    def update(self, request, *args, **kwargs):
        """
        Обновить информацию об интервьюере и очистить кэш.
        """
        instance_id = kwargs.get("pk")
        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            cache.delete_pattern("interviewers_*")
            cache.delete(f"interviewer_{instance_id}")
        return response

    @swagger_auto_schema(
        operation_summary="Частично обновить информацию об интервьюере",
        operation_description="Частично обновить данные интервьюера.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["user_id", "company_id", "position"],
            properties={
                "user_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    example=1,
                    description="ID пользователя, связанного с интервьюером.",
                ),
                "company_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    example=2,
                    description="ID компании, в которой работает интервьюер.",
                ),
                "position": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example="Senior Developer",
                    description="Должность интервьюера.",
                ),
            },
        ),
        responses={
            200: InterviewerSerializer,
            400: "Неверный запрос",
            404: "Интервьюер не найден",
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее интервьюера",
            ),
        ],
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Частично обновить интервьюера и очистить кэш.
        """
        instance_id = kwargs.get("pk")
        response = super().partial_update(request, *args, **kwargs)
        if response.status_code == 200:
            cache.delete_pattern("interviewers_*")
            cache.delete(f"interviewer_{instance_id}")
        return response

    @swagger_auto_schema(
        operation_summary="Удалить интервьюера",
        operation_description="Удалить интервьюера из системы по его ID и очистить соответствующий кэш.",
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее интервьюера",
            ),
        ],
        responses={
            204: openapi.Response(
                description="Интервьюер успешно удален",
                examples={
                    "application/json": None
                },
            ),
            404: openapi.Response(
                description="Интервьюер не найден",
                examples={
                    "application/json": {
                        "detail": "Интервьюер не найден."
                    }
                },
            ),
        },
    )
    def destroy(self, request, *args, **kwargs):
        """
        Удалить интервьюера и очистить кэш.
        """
        instance_id = kwargs.get("pk")
        response = super().destroy(request, *args, **kwargs)
        if response.status_code == 204:
            cache.delete_pattern("interviewers_*")
            cache.delete(f"interviewer_{instance_id}")
        return response

