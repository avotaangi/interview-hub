from rest_framework import viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..models import MultipleChoiceQuestion
from ..serializers.multiple_choice_question_serializer import MultipleChoiceQuestionSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class MultipleChoiceQuestionViewSet(viewsets.ModelViewSet):
    queryset = MultipleChoiceQuestion.objects.all()
    serializer_class = MultipleChoiceQuestionSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['task_item', 'is_correct_answer']

    @swagger_auto_schema(
        operation_summary="Получить список вопросов с выбором ответа",
        operation_description="Возвращает список всех вопросов с выбором ответа, с возможностью фильтрации и пагинации.",
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
                                    "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID вопроса"),
                                    "task_item": openapi.Schema(type=openapi.TYPE_STRING, description="Название задания"),
                                    "answer_text": openapi.Schema(type=openapi.TYPE_STRING, description="Текст ответа"),
                                    "is_correct_answer": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Правильность ответа"),
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
                description="ID задания, к которому привязаны вопросы"
            ),
            openapi.Parameter(
                name="is_correct_answer",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_BOOLEAN,
                description="Фильтр по правильности ответа"
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
        """Список всех вопросов с выбором ответа."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Создать новый вопрос с выбором ответа",
        operation_description="Создает новый вопрос с выбором ответа, привязанный к заданию.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["task_item", "answer_text", "is_correct_answer"],
            properties={
                "task_item": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID задания", example=1),
                "answer_text": openapi.Schema(type=openapi.TYPE_STRING, description="Текст ответа", example="42"),
                "is_correct_answer": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Является ли ответ правильным", example=True),
            }
        ),
        responses={
            201: openapi.Response(
                description="Вопрос успешно создан",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID вопроса"),
                        "task_item": openapi.Schema(type=openapi.TYPE_STRING, description="Название задания"),
                        "answer_text": openapi.Schema(type=openapi.TYPE_STRING, description="Текст ответа"),
                        "is_correct_answer": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Правильность ответа"),
                    }
                )
            ),
            400: "Ошибка в запросе"
        },
    )
    def create(self, request, *args, **kwargs):
        """Создание нового вопроса с выбором ответа."""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Получить вопрос с выбором ответа по ID",
        operation_description="Возвращает данные вопроса с выбором ответа по указанному ID.",
        responses={
            200: openapi.Response(
                description="Успешный ответ",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID вопроса"),
                        "task_item": openapi.Schema(type=openapi.TYPE_STRING, description="Название задания"),
                        "answer_text": openapi.Schema(type=openapi.TYPE_STRING, description="Текст ответа"),
                        "is_correct_answer": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Правильность ответа"),
                    }
                )
            ),
            404: "Вопрос не найден"
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее вопрос"
            ),
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        """Получение вопроса с выбором ответа по ID."""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Обновить вопрос с выбором ответа",
        operation_description="Обновляет данные вопроса с выбором ответа по указанному ID.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["task_item", "answer_text", "is_correct_answer"],
            properties={
                "task_item": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID задания", example=1),
                "answer_text": openapi.Schema(type=openapi.TYPE_STRING, description="Текст ответа", example="43"),
                "is_correct_answer": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Является ли ответ правильным", example=False),
            }
        ),
        responses={
            200: openapi.Response(
                description="Вопрос успешно обновлен",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID вопроса"),
                        "task_item": openapi.Schema(type=openapi.TYPE_STRING, description="Название задания"),
                        "answer_text": openapi.Schema(type=openapi.TYPE_STRING, description="Текст ответа"),
                        "is_correct_answer": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Правильность ответа"),
                    }
                )
            ),
            400: "Ошибка в запросе",
            404: "Вопрос не найден"
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее вопрос"
            ),
        ]
    )
    def update(self, request, *args, **kwargs):
        """Полное обновление вопроса с выбором ответа."""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Частичное обновление вопроса с выбором ответа",
        operation_description="Обновляет указанные поля вопроса с выбором ответа по его ID.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "answer_text": openapi.Schema(type=openapi.TYPE_STRING, description="Обновленный текст ответа", example="44"),
                "is_correct_answer": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Обновленная правильность ответа", example=True),
            }
        ),
        responses={
            200: openapi.Response(
                description="Вопрос успешно обновлен (частично)",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID вопроса"),
                        "task_item": openapi.Schema(type=openapi.TYPE_STRING, description="Название задания"),
                        "answer_text": openapi.Schema(type=openapi.TYPE_STRING, description="Текст ответа"),
                        "is_correct_answer": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Правильность ответа"),
                    }
                )
            ),
            400: "Ошибка в запросе",
            404: "Вопрос не найден"
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее вопрос"
            ),
        ]
    )
    def partial_update(self, request, *args, **kwargs):
        """Частичное обновление вопроса с выбором ответа."""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Удалить вопрос с выбором ответа",
        operation_description="Удаляет вопрос с выбором ответа по его ID.",
        responses={
            204: "Вопрос успешно удален",
            404: "Вопрос не найден"
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее вопрос"
            ),
        ]
    )
    def destroy(self, request, *args, **kwargs):
        """Удаление вопроса с выбором ответа по его ID."""
        return super().destroy(request, *args, **kwargs)
