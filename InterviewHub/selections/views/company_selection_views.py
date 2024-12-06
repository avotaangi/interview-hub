from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from django.db.models import Q
from datetime import timedelta
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..models import CompanySelection
from ..serializers.company_selection_serializers import CompanySelectionSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class CompanySelectionViewSet(viewsets.ModelViewSet):
    queryset = CompanySelection.objects.all()
    serializer_class = CompanySelectionSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["status", "interviewer", "resume"]
    search_fields = ["resume__candidate__user__email", "interviewer__user__email"]

    @swagger_auto_schema(
        operation_summary="Получить список отборов кандидатов",
        operation_description="Возвращает список отборов кандидатов с возможностью фильтрации и поиска.",
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
                                        description="ID отбора",
                                    ),
                                    "interviewer": openapi.Schema(
                                        type=openapi.TYPE_INTEGER,
                                        description="ID интервьюера",
                                    ),
                                    "resume": openapi.Schema(
                                        type=openapi.TYPE_INTEGER,
                                        description="ID резюме",
                                    ),
                                    "status": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="Статус отбора",
                                    ),
                                },
                            ),
                        ),
                    },
                ),
            ),
            400: "Ошибка в запросе",
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Создать новый отбор кандидата",
        operation_description="Создает новый отбор кандидата на основе переданных данных.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["interviewer", "resume", "status"],
            properties={
                "interviewer_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="ID интервьюера"
                ),
                "resume_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="ID резюме"
                ),
                "status": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Статус отбора",
                    enum=["На рассмотрении", "Принят", "Отклонен"],
                ),
            },
        ),
        responses={
            201: openapi.Response(
                description="Отбор успешно создан",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="ID отбора"
                        ),
                        "interviewer": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="ID интервьюера"
                        ),
                        "resume": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="ID резюме"
                        ),
                        "status": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Статус отбора"
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
        operation_summary="Получить отбор кандидата по ID",
        operation_description="Возвращает данные об отборе кандидата по указанному ID.",
        responses={
            200: openapi.Response(
                description="Успешный ответ",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="ID отбора"
                        ),
                        "interviewer": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="ID интервьюера"
                        ),
                        "resume": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="ID резюме"
                        ),
                        "status": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Статус отбора"
                        ),
                    },
                ),
            ),
            404: "Отбор не найден",
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее отбор кандидата",
            ),
        ],
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Обновить отбор кандидата",
        operation_description="Обновляет существующий отбор кандидата по ID.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["interviewer", "resume", "status"],
            properties={
                "interviewer_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="ID интервьюера"
                ),
                "resume_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="ID резюме"
                ),
                "status": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Статус отбора",
                    enum=["На рассмотрении", "Принят", "Отклонен"],
                ),
            },
        ),
        responses={
            200: openapi.Response(
                description="Отбор успешно обновлен",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="ID отбора"
                        ),
                        "interviewer": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="ID интервьюера"
                        ),
                        "resume": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="ID резюме"
                        ),
                        "status": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Статус отбора"
                        ),
                    },
                ),
            ),
            400: "Ошибка в запросе",
            404: "Отбор не найден",
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее отбор кандидата",
            ),
        ],
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Обновить частично отбор кандидата",
        operation_description="Обновляет указанные поля отбора кандидата по ID.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "interviewer_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="ID интервьюера"
                ),
                "resume_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="ID резюме"
                ),
                "status": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Статус отбора",
                    enum=["На рассмотрении", "Принят", "Отклонен"],
                ),
            },
        ),
        responses={
            200: openapi.Response(
                description="Отбор успешно обновлен частично",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="ID отбора"
                        ),
                        "interviewer": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="ID интервьюера"
                        ),
                        "resume": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="ID резюме"
                        ),
                        "status": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Статус отбора"
                        ),
                    },
                ),
            ),
            400: "Ошибка в запросе",
            404: "Отбор не найден",
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее отбор кандидата",
            ),
        ],
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Удалить отбор кандидата",
        operation_description="Удаляет отбор кандидата по указанному ID.",
        responses={204: "Отбор успешно удален", 404: "Отбор не найден"},
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее отбор кандидата",
            ),
        ],
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Обновить статус отбора кандидата",
        operation_description="Обновляет статус отбора кандидата по ID.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["status"],
            properties={
                "status": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Новый статус отбора",
                    enum=["На рассмотрении", "Принят", "Отклонен"],
                )
            },
        ),
        responses={
            200: "Статус успешно обновлен",
            400: "Ошибка в запросе",
            404: "Отбор не найден",
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее отбор кандидата",
            ),
        ],
    )
    @action(detail=True, methods=["patch"], url_path="update-status")
    def update_status(self, request, pk=None):
        """Обновление статуса отбора кандидата."""
        try:
            selection = self.get_object()
        except CompanySelection.DoesNotExist:
            return Response(
                {"detail": "Отбор не найден."}, status=status.HTTP_404_NOT_FOUND
            )

        new_status = request.data.get("status")
        if new_status not in dict(CompanySelection.selection_status_choices).keys():
            return Response(
                {"detail": "Недопустимый статус."}, status=status.HTTP_400_BAD_REQUEST
            )

        selection.status = new_status
        selection.save()
        return Response(
            {"id": selection.id, "status": selection.status}, status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        operation_summary="Фильтрация кандидатов по статусу, возрасту резюме и интервьюеру",
        operation_description=(
            "Фильтрует кандидатов по следующим параметрам:\n"
            "- Статус отбора кандидата: 'На рассмотрении' или 'Принят'.\n"
            "- Исключает кандидатов с резюме, созданным более 7 дней назад.\n"
            "- Отбирает только тех кандидатов, у которых назначен интервьюер."
        ),
        manual_parameters=[
            openapi.Parameter(
                "status",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Фильтрация по статусу отбора кандидата. Разделите несколько статусов запятой, например: 'На рассмотрении,Принят'.",
                required=True,
            ),
        ],
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
                                        description="ID отбора",
                                    ),
                                    "interviewer": openapi.Schema(
                                        type=openapi.TYPE_INTEGER,
                                        description="ID интервьюера",
                                    ),
                                    "resume": openapi.Schema(
                                        type=openapi.TYPE_INTEGER,
                                        description="ID резюме",
                                    ),
                                    "status": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="Статус отбора",
                                    ),
                                },
                            ),
                        ),
                    },
                ),
            ),
            400: "Ошибка в запросе",
        },
    )
    @action(detail=False, methods=["GET"], url_path="practical-filter")
    def practical_filter(self, request):
        # Получаем параметры фильтрации из запроса
        status_filter = request.query_params.get("status", None)

        # Формируем фильтр Q
        q_filter = Q()

        # Фильтрация по статусу отбора кандидата
        if status_filter:
            statuses = status_filter.split(",")  # Статусы передаются через запятую
            status_q = Q()
            for status in statuses:
                status_q |= Q(status=status)  # Логика OR для статусов
            q_filter &= status_q  # Логика AND с другими фильтрами

        # Исключение резюме, отобранных более 7 дней назад
        seven_days_ago = timezone.now() - timedelta(days=7)
        q_filter &= ~Q(
            resume__created_at__lt=seven_days_ago
        )  # Логика NOT для исключения старых резюме

        # Проверка назначения интервьюера
        q_filter &= Q(interviewer__isnull=False)  # Логика AND для наличия интервьюера

        # Применяем фильтрацию на queryset
        selections = self.get_queryset().filter(q_filter)
        page = self.paginate_queryset(selections)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(selections, many=True)
        return Response(serializer.data)
