from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..models import TestTask
from ..serializers.test_task_serializer import TestTaskSerializer

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class TestTaskViewSet(viewsets.ModelViewSet):
    queryset = TestTask.objects.all()
    serializer_class = TestTaskSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["selection", "result"]

    @swagger_auto_schema(
        operation_summary="Получить список тестовых заданий",
        operation_description="Возвращает список всех тестовых заданий с фильтрацией по отбору и результату.",
        responses={
            200: openapi.Response(
                description="Успешный ответ",
                examples={
                    "application/json": {
                        "count": 2,
                        "next": None,
                        "previous": None,
                        "results": [
                            {
                                "id": 1,
                                "selection": 1,
                                "start_time": "2024-12-06T10:00:00Z",
                                "end_time": "2024-12-06T11:00:00Z",
                                "duration": 60,
                                "result": "Принято",
                                "recording_url": "https://example.com/testtask1",
                            },
                            {
                                "id": 2,
                                "selection": 2,
                                "start_time": "2024-12-07T14:00:00Z",
                                "end_time": "2024-12-07T15:00:00Z",
                                "duration": 60,
                                "result": "Отклонено",
                                "recording_url": "https://example.com/testtask2",
                            },
                        ],
                    }
                },
            ),
            400: "Ошибка в запросе",
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Создать тестовое задание",
        operation_description="Создает новое тестовое задание.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["selection", "start_time", "end_time", "duration"],
            properties={
                "selection": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="ID отбора компании",
                    example=1,
                ),
                "start_time": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format="date-time",
                    description="Время начала",
                    example="2024-12-06T10:00:00Z",
                ),
                "end_time": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format="date-time",
                    description="Время окончания",
                    example="2024-12-06T11:00:00Z",
                ),
                "duration": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Продолжительность в минутах",
                    example=60,
                ),
                "result": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Результат задания",
                    enum=["Принято", "Отклонено"],
                    example="Принято",
                ),
                "recording_url": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format="uri",
                    description="Ссылка на запись",
                    example="https://example.com/testtask",
                ),
            },
        ),
        responses={
            201: openapi.Response(
                description="Тестовое задание успешно создано",
                examples={
                    "application/json": {
                        "id": 3,
                        "selection": 1,
                        "start_time": "2024-12-06T10:00:00Z",
                        "end_time": "2024-12-06T11:00:00Z",
                        "duration": 60,
                        "result": "Принято",
                        "recording_url": "https://example.com/testtask",
                    }
                },
            ),
            400: "Ошибка в запросе",
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Получить тестовое задание по ID",
        operation_description="Возвращает информацию о тестовом задании по указанному ID.",
        responses={
            200: openapi.Response(
                description="Успешный ответ",
                examples={
                    "application/json": {
                        "id": 1,
                        "selection": 1,
                        "start_time": "2024-12-06T10:00:00Z",
                        "end_time": "2024-12-06T11:00:00Z",
                        "duration": 60,
                        "result": "Принято",
                        "recording_url": "https://example.com/testtask1",
                    }
                },
            ),
            404: "Тестовое задание не найдено",
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальный идентификатор тестового задания",
            ),
        ],
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Обновить тестовое задание",
        operation_description="Полностью обновляет тестовое задание по его ID.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["selection", "start_time", "end_time", "duration"],
            properties={
                "selection": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="ID отбора компании",
                    example=1,
                ),
                "start_time": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format="date-time",
                    description="Время начала",
                    example="2024-12-06T10:00:00Z",
                ),
                "end_time": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format="date-time",
                    description="Время окончания",
                    example="2024-12-06T11:00:00Z",
                ),
                "duration": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Продолжительность в минутах",
                    example=60,
                ),
                "result": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Результат задания",
                    enum=["Принято", "Отклонено"],
                    example="Принято",
                ),
                "recording_url": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format="uri",
                    description="Ссылка на запись",
                    example="https://example.com/testtask",
                ),
            },
        ),
        responses={
            200: openapi.Response(
                description="Тестовое задание успешно обновлено",
                examples={
                    "application/json": {
                        "id": 1,
                        "selection": 1,
                        "start_time": "2024-12-06T10:00:00Z",
                        "end_time": "2024-12-06T11:00:00Z",
                        "duration": 60,
                        "result": "Принято",
                        "recording_url": "https://example.com/testtask1",
                    }
                },
            ),
            400: "Ошибка в запросе",
            404: "Тестовое задание не найдено",
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальный идентификатор тестового задания",
            ),
        ],
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Частично обновить тестовое задание",
        operation_description="Обновляет указанные поля тестового задания по его ID.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "start_time": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format="date-time",
                    description="Время начала",
                    example="2024-12-06T10:00:00Z",
                ),
                "end_time": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format="date-time",
                    description="Время окончания",
                    example="2024-12-06T11:00:00Z",
                ),
                "duration": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Продолжительность в минутах",
                    example=60,
                ),
                "result": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Результат задания",
                    enum=["Принято", "Отклонено"],
                    example="Принято",
                ),
                "recording_url": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format="uri",
                    description="Ссылка на запись",
                    example="https://example.com/testtask",
                ),
            },
        ),
        responses={
            200: openapi.Response(
                description="Тестовое задание успешно обновлено (частично)",
                examples={
                    "application/json": {
                        "id": 1,
                        "selection": 1,
                        "start_time": "2024-12-06T10:00:00Z",
                        "end_time": "2024-12-06T11:00:00Z",
                        "duration": 60,
                        "result": "Принято",
                        "recording_url": "https://example.com/testtask1",
                    }
                },
            ),
            400: "Ошибка в запросе",
            404: "Тестовое задание не найдено",
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальный идентификатор тестового задания",
            ),
        ],
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Удалить тестовое задание",
        operation_description="Удаляет тестовое задание по его ID.",
        responses={
            204: "Тестовое задание успешно удалено",
            404: "Тестовое задание не найдено",
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальный идентификатор тестового задания",
            ),
        ],
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
