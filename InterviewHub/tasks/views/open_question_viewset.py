from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..models import OpenQuestion
from ..serializers.open_question_serializer import OpenQuestionSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class OpenQuestionViewSet(viewsets.ModelViewSet):
    queryset = OpenQuestion.objects.all()
    serializer_class = OpenQuestionSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['task_item']

    @swagger_auto_schema(
        operation_summary="Получить список заданий с открытым ответом",
        operation_description="Возвращает список всех заданий с открытым ответом, с возможностью фильтрации и пагинации.",
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
                                    "task_item": openapi.Schema(type=openapi.TYPE_STRING, description="Название задания"),
                                    "correct_answer": openapi.Schema(type=openapi.TYPE_STRING, description="Правильный ответ"),
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
                name="task_item",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="ID задания, к которому привязаны задания с открытым ответом"
            ),
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
        ],
    )
    def list(self, request, *args, **kwargs):
        """Список всех заданий с открытым ответом."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Создать новое задание с открытым ответом",
        operation_description="Создает новое задание с открытым ответом, привязанное к заданию.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["task_item", "correct_answer"],
            properties={
                "task_item": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID задания", example=1),
                "correct_answer": openapi.Schema(type=openapi.TYPE_STRING, description="Правильный ответ", example="42"),
            }
        ),
        responses={
            201: openapi.Response(
                description="Задание успешно создано",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID задания"),
                        "task_item": openapi.Schema(type=openapi.TYPE_STRING, description="Название задания"),
                        "correct_answer": openapi.Schema(type=openapi.TYPE_STRING, description="Правильный ответ"),
                    }
                )
            ),
            400: "Ошибка в запросе"
        },
    )
    def create(self, request, *args, **kwargs):
        """Создание нового задания с открытым ответом."""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Получить задание с открытым ответом по ID",
        operation_description="Возвращает данные задания с открытым ответом по указанному ID.",
        responses={
            200: openapi.Response(
                description="Успешный ответ",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID задания"),
                        "task_item": openapi.Schema(type=openapi.TYPE_STRING, description="Название задания"),
                        "correct_answer": openapi.Schema(type=openapi.TYPE_STRING, description="Правильный ответ"),
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
        """Получение задания с открытым ответом по ID."""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Обновить задание с открытым ответом",
        operation_description="Обновляет данные задания с открытым ответом по указанному ID.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["task_item", "correct_answer"],
            properties={
                "task_item": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID задания", example=1),
                "correct_answer": openapi.Schema(type=openapi.TYPE_STRING, description="Правильный ответ", example="43"),
            }
        ),
        responses={
            200: openapi.Response(
                description="Задание успешно обновлено",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID задания"),
                        "task_item": openapi.Schema(type=openapi.TYPE_STRING, description="Название задания"),
                        "correct_answer": openapi.Schema(type=openapi.TYPE_STRING, description="Правильный ответ"),
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
        """Полное обновление задания с открытым ответом."""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Частичное обновление задания с открытым ответом",
        operation_description="Обновляет указанные поля задания с открытым ответом по его ID.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "correct_answer": openapi.Schema(type=openapi.TYPE_STRING, description="Обновленный правильный ответ", example="44"),
            }
        ),
        responses={
            200: openapi.Response(
                description="Задание успешно обновлено (частично)",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID задания"),
                        "task_item": openapi.Schema(type=openapi.TYPE_STRING, description="Название задания"),
                        "correct_answer": openapi.Schema(type=openapi.TYPE_STRING, description="Правильный ответ"),
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
        """Частичное обновление задания с открытым ответом."""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Удалить задание с открытым ответом",
        operation_description="Удаляет задание с открытым ответом по его ID.",
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
        """Удаление задания с открытым ответом по его ID."""
        return super().destroy(request, *args, **kwargs)
