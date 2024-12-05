from rest_framework import viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from tasks.models import CodeQuestion
from tasks.serializers.code_question_serializer import CodeQuestionSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class CodeQuestionViewSet(viewsets.ModelViewSet):
    queryset = CodeQuestion.objects.all()
    serializer_class = CodeQuestionSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['task_item', 'language', 'is_code_run']

    @swagger_auto_schema(
        operation_summary="Получить список заданий с кодом",
        operation_description="Возвращает список всех заданий с написанием кода, с возможностью фильтрации и пагинации.",
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
                                    "language": openapi.Schema(type=openapi.TYPE_STRING, description="Язык программирования"),
                                    "is_code_run": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Был ли выполнен код"),
                                    "code_snippet": openapi.Schema(type=openapi.TYPE_STRING, description="Текст кода"),
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
                description="ID задания, к которому привязаны задания с кодом"
            ),
            openapi.Parameter(
                name="language",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Фильтр по языку программирования"
            ),
            openapi.Parameter(
                name="is_code_run",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_BOOLEAN,
                description="Фильтр по статусу выполнения кода"
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
        """Список всех заданий с кодом."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Создать новое задание с кодом",
        operation_description="Создает новое задание с кодом, привязанное к заданию.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["task_item", "language", "code_snippet"],
            properties={
                "task_item": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID задания", example=1),
                "language": openapi.Schema(type=openapi.TYPE_STRING, description="Язык программирования", example="Python"),
                "is_code_run": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Был ли выполнен код", example=False),
                "code_snippet": openapi.Schema(type=openapi.TYPE_STRING, description="Текст кода", example="print('Hello, World!')"),
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
                        "language": openapi.Schema(type=openapi.TYPE_STRING, description="Язык программирования"),
                        "is_code_run": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Был ли выполнен код"),
                        "code_snippet": openapi.Schema(type=openapi.TYPE_STRING, description="Текст кода"),
                    }
                )
            ),
            400: "Ошибка в запросе"
        },
    )
    def create(self, request, *args, **kwargs):
        """Создание нового задания с кодом."""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Получить задание с кодом по ID",
        operation_description="Возвращает данные задания с кодом по указанному ID.",
        responses={
            200: openapi.Response(
                description="Успешный ответ",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID задания"),
                        "task_item": openapi.Schema(type=openapi.TYPE_STRING, description="Название задания"),
                        "language": openapi.Schema(type=openapi.TYPE_STRING, description="Язык программирования"),
                        "is_code_run": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Был ли выполнен код"),
                        "code_snippet": openapi.Schema(type=openapi.TYPE_STRING, description="Текст кода"),
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
        """Получение задания с кодом по ID."""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Обновить задание с кодом",
        operation_description="Обновляет данные задания с кодом по указанному ID.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["task_item", "language", "code_snippet"],
            properties={
                "task_item": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID задания", example=1),
                "language": openapi.Schema(type=openapi.TYPE_STRING, description="Язык программирования", example="Python"),
                "is_code_run": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Был ли выполнен код", example=True),
                "code_snippet": openapi.Schema(type=openapi.TYPE_STRING, description="Текст кода", example="print('Updated Code')"),
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
                        "language": openapi.Schema(type=openapi.TYPE_STRING, description="Язык программирования"),
                        "is_code_run": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Был ли выполнен код"),
                        "code_snippet": openapi.Schema(type=openapi.TYPE_STRING, description="Текст кода"),
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
        """Полное обновление задания с кодом."""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Частичное обновление задания с кодом",
        operation_description="Обновляет указанные поля задания с кодом по его ID.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "language": openapi.Schema(type=openapi.TYPE_STRING, description="Обновленный язык программирования", example="JavaScript"),
                "code_snippet": openapi.Schema(type=openapi.TYPE_STRING, description="Обновленный текст кода", example="console.log('Hello, World!');"),
                "is_code_run": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Обновленный статус выполнения кода", example=True),
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
                        "language": openapi.Schema(type=openapi.TYPE_STRING, description="Язык программирования"),
                        "is_code_run": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Был ли выполнен код"),
                        "code_snippet": openapi.Schema(type=openapi.TYPE_STRING, description="Текст кода"),
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
        """Частичное обновление задания с кодом."""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Удалить задание с кодом",
        operation_description="Удаляет задание с кодом по его ID.",
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
        """Удаление задания с кодом по его ID."""
        return super().destroy(request, *args, **kwargs)
