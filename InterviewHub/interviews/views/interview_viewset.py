from rest_framework import viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..models import Interview, InterviewTaskItem
from ..serializers.interview_serializer import InterviewSerializer
from ..serializers.interview_task_serializer import InterviewTaskItemDetailSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class InterviewViewSet(viewsets.ModelViewSet):
    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['selection', 'status', 'result']

    @swagger_auto_schema(
        operation_summary="Получить список интервью",
        operation_description=(
            "Возвращает список всех интервью с возможностью фильтрации по отбору, статусу, "
            "результату и пагинации. Поддерживаются следующие фильтры:\n\n"
            "- **selection**: Фильтрация по ID отбора кандидата.\n"
            "- **status**: Фильтрация по статусу интервью (например, 'Запланировано').\n"
            "- **result**: Фильтрация по результату интервью (например, 'Принято')."
        ),
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
                                    "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID интервью"),
                                    "selection": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID отбора кандидата"),
                                    "start_time": openapi.Schema(type=openapi.TYPE_STRING, format="date-time", description="Время начала"),
                                    "end_time": openapi.Schema(type=openapi.TYPE_STRING, format="date-time", description="Время окончания"),
                                    "duration": openapi.Schema(type=openapi.TYPE_INTEGER, description="Продолжительность интервью в минутах"),
                                    "type": openapi.Schema(type=openapi.TYPE_STRING, description="Тип интервью"),
                                    "status": openapi.Schema(type=openapi.TYPE_STRING, description="Статус интервью"),
                                    "feedback": openapi.Schema(type=openapi.TYPE_STRING, description="Обратная связь"),
                                    "notes": openapi.Schema(type=openapi.TYPE_STRING, description="Примечания"),
                                    "hard_skills_rate": openapi.Schema(type=openapi.TYPE_INTEGER, description="Оценка хард-скиллов"),
                                    "soft_skills_rate": openapi.Schema(type=openapi.TYPE_INTEGER, description="Оценка софт-скиллов"),
                                    "result": openapi.Schema(type=openapi.TYPE_STRING, description="Результат интервью"),
                                    "recording_url": openapi.Schema(type=openapi.TYPE_STRING, format="uri", description="URL записи интервью"),
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
                name="selection",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Фильтр по ID отбора кандидата"
            ),
            openapi.Parameter(
                name="status",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Фильтр по статусу интервью"
            ),
            openapi.Parameter(
                name="result",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Фильтр по результату интервью"
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
        """Возвращает список всех интервью с фильтрацией и пагинацией."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Создать новое интервью",
        operation_description=(
            "Создает новое интервью, связанное с указанным ID отбора кандидата. "
            "Обязательно указать начальное и конечное время, тип интервью, а также его статус."
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["selection", "start_time", "end_time", "type", "status"],
            properties={
                "selection": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID отбора кандидата", example=1),
                "start_time": openapi.Schema(type=openapi.TYPE_STRING, format="date-time", description="Время начала", example="2024-12-06T10:00:00Z"),
                "end_time": openapi.Schema(type=openapi.TYPE_STRING, format="date-time", description="Время окончания", example="2024-12-06T11:00:00Z"),
                "type": openapi.Schema(type=openapi.TYPE_STRING, description="Тип интервью (например, 'Техническое')", example="Техническое"),
                "status": openapi.Schema(type=openapi.TYPE_STRING, description="Статус интервью", example="Запланировано"),
                "feedback": openapi.Schema(type=openapi.TYPE_STRING, description="Обратная связь (если есть)", example="Кандидат показал хороший уровень."),
                "notes": openapi.Schema(type=openapi.TYPE_STRING, description="Примечания (если есть)", example="Проверить хард-скиллы."),
                "hard_skills_rate": openapi.Schema(type=openapi.TYPE_INTEGER, description="Оценка хард-скиллов (от 0 до 10)", example=8),
                "soft_skills_rate": openapi.Schema(type=openapi.TYPE_INTEGER, description="Оценка софт-скиллов (от 0 до 10)", example=7),
                "result": openapi.Schema(type=openapi.TYPE_STRING, description="Результат интервью", example="Принято"),
                "recording_url": openapi.Schema(type=openapi.TYPE_STRING, format="uri", description="Ссылка на запись интервью", example="https://example.com/interview-recording"),
            }
        ),
        responses={
            201: openapi.Response(
                description="Интервью успешно создано",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID интервью"),
                        "selection": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID отбора кандидата"),
                        "start_time": openapi.Schema(type=openapi.TYPE_STRING, format="date-time", description="Время начала"),
                        "end_time": openapi.Schema(type=openapi.TYPE_STRING, format="date-time", description="Время окончания"),
                        "duration": openapi.Schema(type=openapi.TYPE_INTEGER, description="Продолжительность интервью в минутах"),
                        "type": openapi.Schema(type=openapi.TYPE_STRING, description="Тип интервью"),
                        "status": openapi.Schema(type=openapi.TYPE_STRING, description="Статус интервью"),
                        "feedback": openapi.Schema(type=openapi.TYPE_STRING, description="Обратная связь"),
                        "notes": openapi.Schema(type=openapi.TYPE_STRING, description="Примечания"),
                        "hard_skills_rate": openapi.Schema(type=openapi.TYPE_INTEGER, description="Оценка хард-скиллов"),
                        "soft_skills_rate": openapi.Schema(type=openapi.TYPE_INTEGER, description="Оценка софт-скиллов"),
                        "result": openapi.Schema(type=openapi.TYPE_STRING, description="Результат интервью"),
                        "recording_url": openapi.Schema(type=openapi.TYPE_STRING, format="uri", description="Ссылка на запись интервью"),
                    }
                )
            ),
            400: "Ошибка в запросе"
        },
    )
    def create(self, request, *args, **kwargs):
        """Создает новое интервью, связанное с указанным отбором."""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Получить интервью по ID",
        operation_description="Возвращает данные интервью по указанному ID.",
        responses={
            200: openapi.Response(
                description="Успешный ответ",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID интервью"),
                        "selection": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID отбора кандидата"),
                        "start_time": openapi.Schema(type=openapi.TYPE_STRING, format="date-time", description="Время начала"),
                        "end_time": openapi.Schema(type=openapi.TYPE_STRING, format="date-time", description="Время окончания"),
                        "duration": openapi.Schema(type=openapi.TYPE_INTEGER, description="Продолжительность интервью в минутах"),
                        "type": openapi.Schema(type=openapi.TYPE_STRING, description="Тип интервью"),
                        "status": openapi.Schema(type=openapi.TYPE_STRING, description="Статус интервью"),
                        "feedback": openapi.Schema(type=openapi.TYPE_STRING, description="Обратная связь"),
                        "notes": openapi.Schema(type=openapi.TYPE_STRING, description="Примечания"),
                        "hard_skills_rate": openapi.Schema(type=openapi.TYPE_INTEGER, description="Оценка хард-скиллов"),
                        "soft_skills_rate": openapi.Schema(type=openapi.TYPE_INTEGER, description="Оценка софт-скиллов"),
                        "result": openapi.Schema(type=openapi.TYPE_STRING, description="Результат интервью"),
                        "recording_url": openapi.Schema(type=openapi.TYPE_STRING, format="uri", description="Ссылка на запись интервью"),
                    }
                )
            ),
            404: "Интервью не найдено"
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальный идентификатор интервью"
            ),
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        """Возвращает интервью по ID."""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Частичное обновление интервью",
        operation_description=(
                "Обновляет указанные поля интервью по ID. Позволяет обновить статус, результат, обратную связь и другие данные.\n\n"
                "Поддерживаются следующие поля для обновления:\n"
                "- **status**: Обновление статуса интервью (например, 'Завершено').\n"
                "- **feedback**: Добавление или изменение обратной связи.\n"
                "- **notes**: Примечания к интервью.\n"
                "- **result**: Результат интервью (например, 'Принято')."
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(type=openapi.TYPE_STRING, description="Обновленный статус интервью",
                                         example="Завершено"),
                "feedback": openapi.Schema(type=openapi.TYPE_STRING, description="Обратная связь",
                                           example="Кандидат показал отличный результат."),
                "notes": openapi.Schema(type=openapi.TYPE_STRING, description="Примечания",
                                        example="Рекомендовано проверить софт-скиллы."),
                "result": openapi.Schema(type=openapi.TYPE_STRING, description="Результат интервью", example="Принято"),
                "hard_skills_rate": openapi.Schema(type=openapi.TYPE_INTEGER, description="Оценка хард-скиллов",
                                                   example=9),
                "soft_skills_rate": openapi.Schema(type=openapi.TYPE_INTEGER, description="Оценка софт-скиллов",
                                                   example=8),
            }
        ),
        responses={
            200: openapi.Response(
                description="Интервью успешно обновлено (частично)",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID интервью"),
                        "status": openapi.Schema(type=openapi.TYPE_STRING, description="Обновленный статус интервью"),
                        "feedback": openapi.Schema(type=openapi.TYPE_STRING, description="Обновленная обратная связь"),
                        "notes": openapi.Schema(type=openapi.TYPE_STRING, description="Примечания"),
                        "result": openapi.Schema(type=openapi.TYPE_STRING,
                                                 description="Обновленный результат интервью"),
                        "hard_skills_rate": openapi.Schema(type=openapi.TYPE_INTEGER,
                                                           description="Оценка хард-скиллов"),
                        "soft_skills_rate": openapi.Schema(type=openapi.TYPE_INTEGER,
                                                           description="Оценка софт-скиллов"),
                    }
                )
            ),
            400: "Ошибка в запросе",
            404: "Интервью не найдено"
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальный идентификатор интервью"
            ),
        ]
    )
    def partial_update(self, request, *args, **kwargs):
        """Частичное обновление интервью (PATCH)."""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Полное обновление интервью",
        operation_description=(
                "Полностью обновляет данные интервью по ID. Требуется указать все обязательные поля, включая "
                "ID отбора, начальное и конечное время, тип и статус интервью."
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["selection", "start_time", "end_time", "type", "status"],
            properties={
                "selection": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID отбора кандидата", example=1),
                "start_time": openapi.Schema(type=openapi.TYPE_STRING, format="date-time", description="Время начала",
                                             example="2024-12-06T10:00:00Z"),
                "end_time": openapi.Schema(type=openapi.TYPE_STRING, format="date-time", description="Время окончания",
                                           example="2024-12-06T11:00:00Z"),
                "type": openapi.Schema(type=openapi.TYPE_STRING, description="Тип интервью", example="Техническое"),
                "status": openapi.Schema(type=openapi.TYPE_STRING, description="Статус интервью",
                                         example="Запланировано"),
                "feedback": openapi.Schema(type=openapi.TYPE_STRING, description="Обратная связь",
                                           example="Кандидат показал высокий уровень."),
                "notes": openapi.Schema(type=openapi.TYPE_STRING, description="Примечания",
                                        example="Проверить знания хард-скиллов."),
                "hard_skills_rate": openapi.Schema(type=openapi.TYPE_INTEGER, description="Оценка хард-скиллов",
                                                   example=9),
                "soft_skills_rate": openapi.Schema(type=openapi.TYPE_INTEGER, description="Оценка софт-скиллов",
                                                   example=8),
                "result": openapi.Schema(type=openapi.TYPE_STRING, description="Результат интервью", example="Принято"),
                "recording_url": openapi.Schema(type=openapi.TYPE_STRING, format="uri", description="Ссылка на запись",
                                                example="https://example.com/recording"),
            }
        ),
        responses={
            200: openapi.Response(
                description="Интервью успешно обновлено",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID интервью"),
                        "selection": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID отбора кандидата"),
                        "start_time": openapi.Schema(type=openapi.TYPE_STRING, format="date-time",
                                                     description="Время начала"),
                        "end_time": openapi.Schema(type=openapi.TYPE_STRING, format="date-time",
                                                   description="Время окончания"),
                        "duration": openapi.Schema(type=openapi.TYPE_INTEGER,
                                                   description="Продолжительность интервью в минутах"),
                        "type": openapi.Schema(type=openapi.TYPE_STRING, description="Тип интервью"),
                        "status": openapi.Schema(type=openapi.TYPE_STRING, description="Обновленный статус интервью"),
                        "feedback": openapi.Schema(type=openapi.TYPE_STRING, description="Обновленная обратная связь"),
                        "notes": openapi.Schema(type=openapi.TYPE_STRING, description="Примечания"),
                        "hard_skills_rate": openapi.Schema(type=openapi.TYPE_INTEGER,
                                                           description="Оценка хард-скиллов"),
                        "soft_skills_rate": openapi.Schema(type=openapi.TYPE_INTEGER,
                                                           description="Оценка софт-скиллов"),
                        "result": openapi.Schema(type=openapi.TYPE_STRING, description="Результат интервью"),
                        "recording_url": openapi.Schema(type=openapi.TYPE_STRING, format="uri",
                                                        description="Ссылка на запись интервью"),
                    }
                )
            ),
            400: "Ошибка в запросе",
            404: "Интервью не найдено"
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальный идентификатор интервью"
            ),
        ]
    )
    def update(self, request, *args, **kwargs):
        """Полное обновление интервью (PUT)."""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Удалить интервью",
        operation_description="Удаляет интервью по указанному ID.",
        responses={
            204: "Интервью успешно удалено",
            404: "Интервью не найдено"
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальный идентификатор интервью"
            ),
        ]
    )
    def destroy(self, request, *args, **kwargs):
        """Удаляет интервью по его ID."""
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Получить задания, связанные с интервью",
        operation_description=(
                "Возвращает список всех заданий, связанных с указанным интервью. "
                "Каждый элемент включает информацию о задании, решении кандидата и правильных ответах (если есть)."
        ),
        responses={
            200: openapi.Response(
                description="Успешный ответ",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "interview_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID интервью"),
                        "tasks": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "task": openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            "task_id": openapi.Schema(type=openapi.TYPE_INTEGER,
                                                                      description="ID задания"),
                                            "title": openapi.Schema(type=openapi.TYPE_STRING,
                                                                    description="Название задания"),
                                            "complexity": openapi.Schema(type=openapi.TYPE_INTEGER,
                                                                         description="Сложность задания"),
                                            "task_condition": openapi.Schema(type=openapi.TYPE_STRING,
                                                                             description="Условие задания"),
                                        }
                                    ),
                                    "candidate_answer": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="Ответ кандидата"
                                    ),
                                    "correct_answers": openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            "open_question": openapi.Schema(
                                                type=openapi.TYPE_STRING,
                                                description="Правильный ответ для открытого задания",
                                                nullable=True
                                            ),
                                            "multiple_choice": openapi.Schema(
                                                type=openapi.TYPE_ARRAY,
                                                items=openapi.Schema(
                                                    type=openapi.TYPE_STRING
                                                ),
                                                description="Список правильных ответов для задания с выбором",
                                                nullable=True
                                            ),
                                            "code_question": openapi.Schema(
                                                type=openapi.TYPE_OBJECT,
                                                properties={
                                                    "language": openapi.Schema(type=openapi.TYPE_STRING,
                                                                               description="Язык программирования"),
                                                    "code_snippet": openapi.Schema(type=openapi.TYPE_STRING,
                                                                                   description="Правильный код"),
                                                },
                                                nullable=True
                                            )
                                        }
                                    ),
                                }
                            )
                        )
                    }
                )
            ),
            404: "Интервью или задания не найдены"
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальный идентификатор интервью"
            ),
        ]
    )
    @action(detail=True, methods=['get'], url_path="tasks")
    def get_tasks(self, request, pk=None):
        """
        Возвращает задания, связанные с интервью.
        """
        try:
            interview = self.get_object()
        except Interview.DoesNotExist:
            return Response({"detail": "Интервью не найдено."}, status=status.HTTP_404_NOT_FOUND)

        # Получение всех заданий, связанных с интервью
        tasks = InterviewTaskItem.objects.filter(interview=interview).select_related('task_item')

        # Использование сериализатора для формирования ответа
        serializer = InterviewTaskItemDetailSerializer(tasks, many=True)

        return Response(
            {
                "interview_id": interview.id,
                "tasks": serializer.data,
            },
            status=status.HTTP_200_OK
        )