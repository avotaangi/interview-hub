from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..models import InterviewTaskItem
from ..serializers.interview_task_serializer import InterviewTaskItemSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class InterviewTaskItemViewSet(viewsets.ModelViewSet):
    queryset = InterviewTaskItem.objects.all()
    serializer_class = InterviewTaskItemSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["interview", "task_item"]

    @swagger_auto_schema(
        operation_summary="Получить список элементов заданий к интервью",
        operation_description=(
            "Возвращает список всех элементов заданий к интервью с возможностью фильтрации и пагинации. "
            "Поддерживаются следующие фильтры:\n\n"
            "- **interview**: Фильтрация по ID интервью.\n"
            "- **task_item**: Фильтрация по ID задания."
        ),
        responses={
            200: openapi.Response(
                description="Успешный ответ",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "count": openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="Общее количество элементов",
                        ),
                        "next": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Ссылка на следующую страницу",
                        ),
                        "previous": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Ссылка на предыдущую страницу",
                        ),
                        "results": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "id": openapi.Schema(
                                        type=openapi.TYPE_INTEGER,
                                        description="ID элемента задания",
                                    ),
                                    "interview": openapi.Schema(
                                        type=openapi.TYPE_INTEGER,
                                        description="ID интервью",
                                    ),
                                    "task_item": openapi.Schema(
                                        type=openapi.TYPE_INTEGER,
                                        description="ID задания",
                                    ),
                                    "candidate_answer": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="Ответ кандидата",
                                    ),
                                },
                            ),
                        ),
                    },
                ),
            ),
            400: "Ошибка в запросе",
        },
        manual_parameters=[
            openapi.Parameter(
                name="interview",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Фильтр по ID интервью",
            ),
            openapi.Parameter(
                name="task_item",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Фильтр по ID задания",
            ),
            openapi.Parameter(
                name="page",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Номер страницы для пагинации",
            ),
            openapi.Parameter(
                name="page_size",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Количество элементов на странице",
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        """Возвращает список всех элементов заданий к интервью с фильтрацией и пагинацией."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Создать новый элемент задания к интервью",
        operation_description="Создает новый элемент задания, связанный с указанным интервью.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["interview", "task_item", "candidate_answer"],
            properties={
                "interview": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="ID интервью", example=1
                ),
                "task_item": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="ID задания", example=101
                ),
                "candidate_answer": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Ответ кандидата",
                    example="Ответ на задание.",
                ),
            },
        ),
        responses={
            201: openapi.Response(
                description="Элемент задания успешно создан",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="ID элемента задания"
                        ),
                        "interview": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="ID интервью"
                        ),
                        "task_item": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="ID задания"
                        ),
                        "candidate_answer": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Ответ кандидата"
                        ),
                    },
                ),
            ),
            400: "Ошибка в запросе",
        },
    )
    def create(self, request, *args, **kwargs):
        """Создает новый элемент задания к интервью."""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Получить элемент задания по ID",
        operation_description="Возвращает данные элемента задания по указанному ID.",
        responses={
            200: openapi.Response(
                description="Успешный ответ",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="ID элемента задания"
                        ),
                        "interview": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="ID интервью"
                        ),
                        "task_item": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="ID задания"
                        ),
                        "candidate_answer": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Ответ кандидата"
                        ),
                    },
                ),
            ),
            404: "Элемент задания не найден",
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальный идентификатор элемента задания",
            ),
        ],
    )
    def retrieve(self, request, *args, **kwargs):
        """Возвращает элемент задания по ID."""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Обновить элемент задания к интервью",
        operation_description="Полностью обновляет данные элемента задания по его ID.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["interview", "task_item", "candidate_answer"],
            properties={
                "interview": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="ID интервью", example=1
                ),
                "task_item": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="ID задания", example=102
                ),
                "candidate_answer": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Обновленный ответ кандидата",
                    example="Обновленный ответ.",
                ),
            },
        ),
        responses={
            200: openapi.Response(
                description="Элемент задания успешно обновлен",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="ID элемента задания"
                        ),
                        "interview": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="ID интервью"
                        ),
                        "task_item": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="ID задания"
                        ),
                        "candidate_answer": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Обновленный ответ кандидата",
                        ),
                    },
                ),
            ),
            400: "Ошибка в запросе",
            404: "Элемент задания не найден",
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальный идентификатор элемента задания",
            ),
        ],
    )
    def update(self, request, *args, **kwargs):
        """Полностью обновляет элемент задания к интервью."""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Частично обновить элемент задания к интервью",
        operation_description="Обновляет указанные поля элемента задания по его ID.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "candidate_answer": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Обновленный ответ кандидата",
                    example="Новый ответ.",
                ),
            },
        ),
        responses={
            200: openapi.Response(
                description="Элемент задания успешно обновлен (частично)",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="ID элемента задания"
                        ),
                        "interview": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="ID интервью"
                        ),
                        "task_item": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="ID задания"
                        ),
                        "candidate_answer": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Обновленный ответ кандидата",
                        ),
                    },
                ),
            ),
            400: "Ошибка в запросе",
            404: "Элемент задания не найден",
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальный идентификатор элемента задания",
            ),
        ],
    )
    def partial_update(self, request, *args, **kwargs):
        """Частично обновляет элемент задания к интервью."""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Удалить элемент задания к интервью",
        operation_description="Удаляет элемент задания к интервью по его ID.",
        responses={
            204: "Элемент задания успешно удален",
            404: "Элемент задания не найден",
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальный идентификатор элемента задания",
            ),
        ],
    )
    def destroy(self, request, *args, **kwargs):
        """Удаляет элемент задания к интервью по его ID."""
        return super().destroy(request, *args, **kwargs)
