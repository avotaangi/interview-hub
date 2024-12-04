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
from ..models import JobExperience
from ..serializers import JobSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class JobViewSet(viewsets.ModelViewSet):
    queryset = JobExperience.objects.all()
    serializer_class = JobSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['company', 'position', 'start_date', 'end_date']
    search_fields = ['company', 'position', 'responsibilities']

    @swagger_auto_schema(
        operation_summary="Получить список работ",
        operation_description="Возвращает список записей о работах с возможностью фильтрации, поиска и пагинации.",
        responses={
            200: openapi.Response(
                description="Успешный ответ",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "count": openapi.Schema(type=openapi.TYPE_INTEGER, description="Общее количество записей"),
                        "next": openapi.Schema(type=openapi.TYPE_STRING, description="Ссылка на следующую страницу"),
                        "previous": openapi.Schema(type=openapi.TYPE_STRING,
                                                   description="Ссылка на предыдущую страницу"),
                        "results": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID записи"),
                                    "company": openapi.Schema(type=openapi.TYPE_STRING,
                                                              description="Название компании"),
                                    "position": openapi.Schema(type=openapi.TYPE_STRING,
                                                               description="Название должности"),
                                    "start_date": openapi.Schema(type=openapi.TYPE_STRING, format="date",
                                                                 description="Дата начала работы"),
                                    "end_date": openapi.Schema(type=openapi.TYPE_STRING, format="date",
                                                               description="Дата окончания работы"),
                                    "responsibilities": openapi.Schema(type=openapi.TYPE_STRING,
                                                                       description="Основные обязанности"),
                                }
                            ),
                        ),
                    },
                ),
            ),
            400: "Ошибка в запросе"
        },
        manual_parameters=[
            openapi.Parameter(name="search", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              description="Поиск по компании, должности или обязанностям"),
            openapi.Parameter(name="company", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              description="Поиск по компании"),
            openapi.Parameter(name="position", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              description="Поиск по должности"),
            openapi.Parameter(name="start_date", in_=openapi.IN_QUERY, type=openapi.FORMAT_DATE,
                              description="Поиск по началу времени"),
            openapi.Parameter(name="end_date", in_=openapi.IN_QUERY, type=openapi.FORMAT_DATE,
                              description="Поиск по концу времени"),
            openapi.Parameter(name="page", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description="Номер страницы для пагинации"),
            openapi.Parameter(name="page_size", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description="Количество записей на странице"),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Создать новую запись о работе",
        operation_description="Создает новую запись о работе. Обязательно укажите название компании, должность, дату начала работы.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["company", "position", "start_date"],
            properties={
                "company": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Название компании",
                    example="INNOPROG"
                ),
                "position": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Название должности",
                    example="Software Developer"
                ),
                "start_date": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format="date",
                    description="Дата начала работы",
                    example="2024-01-01"
                ),
                "end_date": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format="date",
                    description="Дата окончания работы",
                    example="2024-11-30"
                ),
                "responsibilities": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Основные обязанности",
                    example="Разработка и поддержка веб-приложений."
                ),
            },
        ),
        responses={
            201: openapi.Response(
                description="Запись успешно создана",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="ID записи",
                            example=1
                        ),
                        "company": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Название компании",
                            example="OpenAI"
                        ),
                        "position": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Название должности",
                            example="Software Developer"
                        ),
                        "start_date": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            format="date",
                            description="Дата начала работы",
                            example="2023-01-01"
                        ),
                        "end_date": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            format="date",
                            description="Дата окончания работы",
                            example="2023-12-30"
                        ),
                        "responsibilities": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Основные обязанности",
                            example="Разработка и поддержка веб-приложений."
                        ),
                    },
                ),
            ),
            400: "Ошибка в запросе",
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Получить запись о работе по ID",
        operation_description="Возвращает данные о записи работы на основе указанного ID.",
        responses={
            200: openapi.Response(
                description="Успешный ответ",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID записи"),
                        "company": openapi.Schema(type=openapi.TYPE_STRING, description="Название компании"),
                        "position": openapi.Schema(type=openapi.TYPE_STRING, description="Название должности"),
                        "start_date": openapi.Schema(type=openapi.TYPE_STRING, format="date",
                                                     description="Дата начала работы"),
                        "end_date": openapi.Schema(type=openapi.TYPE_STRING, format="date",
                                                   description="Дата окончания работы"),
                        "responsibilities": openapi.Schema(type=openapi.TYPE_STRING,
                                                           description="Основные обязанности"),
                    },
                ),
            ),
            404: "Запись о работе не найдена",
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее запись о работе",
            ),
        ],
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Обновить запись о работе",
        operation_description="Полностью обновляет запись о работе по ID. Обновляемые данные должны быть переданы в теле запроса.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["company", "position", "start_date"],
            properties={
                "company": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Название компании",
                    example="INNOPROG"
                ),
                "position": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Название должности",
                    example="Software Developer"
                ),
                "start_date": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format="date",
                    description="Дата начала работы",
                    example="2024-01-01"
                ),
                "end_date": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format="date",
                    description="Дата окончания работы",
                    example="2024-11-30"
                ),
                "responsibilities": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Основные обязанности",
                    example="Разработка и поддержка веб-приложений."
                ),
            },
        ),
        responses={
            200: openapi.Response(
                description="Запись успешно обновлена",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="ID записи",
                            example=1
                        ),
                        "company": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Название компании",
                            example="OpenAI"
                        ),
                        "position": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Название должности",
                            example="Software Developer"
                        ),
                        "start_date": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            format="date",
                            description="Дата начала работы",
                            example="2023-01-01"
                        ),
                        "end_date": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            format="date",
                            description="Дата окончания работы",
                            example="2023-12-30"
                        ),
                        "responsibilities": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Основные обязанности",
                            example="Разработка и поддержка веб-приложений."
                        ),
                    },
                ),
            ),
            400: "Ошибка в запросе",
            404: "Запись о работе не найдена",
        },
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Частично обновить запись о работе",
        operation_description="Частично обновляет указанные поля записи о работе по ID.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "company": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Название компании",
                    example="INNOPROG"
                ),
                "position": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Название должности",
                    example="Software Developer"
                ),
                "start_date": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format="date",
                    description="Дата начала работы",
                    example="2024-01-01"
                ),
                "end_date": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format="date",
                    description="Дата окончания работы",
                    example="2024-11-30"
                ),
                "responsibilities": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Основные обязанности",
                    example="Разработка и поддержка веб-приложений."
                ),
            },
        ),
        responses={
            200: openapi.Response(
                description="Запись успешно обновлена",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="ID записи",
                            example=1
                        ),
                        "company": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Название компании",
                            example="OpenAI"
                        ),
                        "position": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Название должности",
                            example="Software Developer"
                        ),
                        "start_date": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            format="date",
                            description="Дата начала работы",
                            example="2023-01-01"
                        ),
                        "end_date": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            format="date",
                            description="Дата окончания работы",
                            example="2023-12-30"
                        ),
                        "responsibilities": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Основные обязанности",
                            example="Разработка и поддержка веб-приложений."
                        ),
                    },
                ),
            ),
            400: "Ошибка в запросе",
            404: "Запись о работе не найдена",
        },
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Удалить запись о работе",
        operation_description="Удаляет запись о работе на основе указанного ID.",
        responses={
            204: "Запись успешно удалена",
            404: "Запись о работе не найдена",
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее запись о работе",
            ),
        ],
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
