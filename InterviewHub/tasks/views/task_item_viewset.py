from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..models import TaskItem
from ..serializers.task_item_serializer import TaskItemSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class TaskItemViewSet(viewsets.ModelViewSet):
    queryset = TaskItem.objects.all()
    serializer_class = TaskItemSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['complexity']
    search_fields = ['title', 'task_condition']

    @swagger_auto_schema(
        operation_summary="Получить список заданий",
        operation_description="Возвращает список заданий с возможностью фильтрации, поиска и пагинации.",
        responses={
            200: openapi.Response(
                description="Успешный ответ",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "count": openapi.Schema(type=openapi.TYPE_INTEGER, description="Общее количество элементов"),
                        "next": openapi.Schema(type=openapi.TYPE_STRING, description="Ссылка на следующую страницу"),
                        "previous": openapi.Schema(type=openapi.TYPE_STRING, description="Ссылка на предыдущую страницу"),
                        "results": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID задания"),
                                    "title": openapi.Schema(type=openapi.TYPE_STRING, description="Название задания"),
                                    "complexity": openapi.Schema(type=openapi.TYPE_INTEGER, description="Сложность задания"),
                                    "task_condition": openapi.Schema(type=openapi.TYPE_STRING, description="Условие задания"),
                                }
                            ),
                        ),
                    },
                ),
            ),
            400: "Ошибка в запросе"
        },
        manual_parameters=[
            openapi.Parameter(
                name="page",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Номер страницы для пагинации"
            ),
            openapi.Parameter(
                name="page_size",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Количество элементов на странице"
            ),
            openapi.Parameter(
                name="complexity",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Фильтр по сложности задания"
            ),
            openapi.Parameter(
                name="search",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Поиск по названию или условию задания"
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        """Список всех заданий с поддержкой фильтров, поиска и пагинации."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Создать новое задание",
        operation_description="Создает новое задание с указанными данными.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["title", "complexity", "task_condition"],
            properties={
                "title": openapi.Schema(type=openapi.TYPE_STRING, description="Название задания", example="Алгоритм сортировки"),
                "complexity": openapi.Schema(type=openapi.TYPE_INTEGER, description="Сложность задания", example=3),
                "task_condition": openapi.Schema(type=openapi.TYPE_STRING, description="Условие задания", example="Написать алгоритм сортировки массива.")
            }
        ),
        responses={
            201: openapi.Response(
                description="Задание успешно создано",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID задания"),
                        "title": openapi.Schema(type=openapi.TYPE_STRING, description="Название задания"),
                        "complexity": openapi.Schema(type=openapi.TYPE_INTEGER, description="Сложность задания"),
                        "task_condition": openapi.Schema(type=openapi.TYPE_STRING, description="Условие задания"),
                    }
                )
            ),
            400: "Ошибка в запросе"
        },
    )
    def create(self, request, *args, **kwargs):
        """Создание нового задания."""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Получить задание по ID",
        operation_description="Возвращает данные задания по указанному ID.",
        responses={
            200: openapi.Response(
                description="Успешный ответ",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID задания"),
                        "title": openapi.Schema(type=openapi.TYPE_STRING, description="Название задания"),
                        "complexity": openapi.Schema(type=openapi.TYPE_INTEGER, description="Сложность задания"),
                        "task_condition": openapi.Schema(type=openapi.TYPE_STRING, description="Условие задания"),
                    }
                )
            ),
            404: "Задание не найдено"
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее задание"
            ),
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        """Получение конкретного задания по его ID."""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Обновить задание",
        operation_description="Обновляет данные задания по указанному ID.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["title", "complexity", "task_condition"],
            properties={
                "title": openapi.Schema(type=openapi.TYPE_STRING, description="Название задания", example="Алгоритм поиска"),
                "complexity": openapi.Schema(type=openapi.TYPE_INTEGER, description="Сложность задания", example=2),
                "task_condition": openapi.Schema(type=openapi.TYPE_STRING, description="Условие задания", example="Написать алгоритм поиска элемента в массиве.")
            }
        ),
        responses={
            200: openapi.Response(
                description="Задание успешно обновлено",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID задания"),
                        "title": openapi.Schema(type=openapi.TYPE_STRING, description="Название задания"),
                        "complexity": openapi.Schema(type=openapi.TYPE_INTEGER, description="Сложность задания"),
                        "task_condition": openapi.Schema(type=openapi.TYPE_STRING, description="Условие задания"),
                    }
                )
            ),
            400: "Ошибка в запросе",
            404: "Задание не найдено"
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее задание"
            ),
        ]
    )
    def update(self, request, *args, **kwargs):
        """Полное обновление задания."""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Частичное обновление задания",
        operation_description="Обновляет указанные поля задания по его ID.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "title": openapi.Schema(type=openapi.TYPE_STRING, description="Название задания", example="Алгоритм поиска"),
                "complexity": openapi.Schema(type=openapi.TYPE_INTEGER, description="Сложность задания", example=2),
                "task_condition": openapi.Schema(type=openapi.TYPE_STRING, description="Условие задания", example="Обновите описание задания."),
            }
        ),
        responses={
            200: openapi.Response(
                description="Задание успешно обновлено (частично)",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID задания"),
                        "title": openapi.Schema(type=openapi.TYPE_STRING, description="Название задания"),
                        "complexity": openapi.Schema(type=openapi.TYPE_INTEGER, description="Сложность задания"),
                        "task_condition": openapi.Schema(type=openapi.TYPE_STRING, description="Условие задания"),
                    }
                )
            ),
            400: "Ошибка в запросе",
            404: "Задание не найдено"
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее задание"
            ),
        ]
    )
    def partial_update(self, request, *args, **kwargs):
        """Частичное обновление задания."""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Удалить задание",
        operation_description="Удаляет задание по его ID.",
        responses={
            204: "Задание успешно удалено",
            404: "Задание не найдено"
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее задание"
            ),
        ]
    )
    def destroy(self, request, *args, **kwargs):
        """Удаление задания по его ID."""
        return super().destroy(request, *args, **kwargs)
