from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..models import TestTaskItem
from ..serializers.test_task_item_serializer import TestTaskItemSerializer


class TestTaskItemViewSet(viewsets.ModelViewSet):
    queryset = TestTaskItem.objects.all()
    serializer_class = TestTaskItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["test_task", "task_item"]

    @swagger_auto_schema(
        operation_summary="Получить список элементов заданий",
        operation_description="Возвращает список всех элементов заданий, связанных с тестовыми заданиями.",
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
                                "test_task": 1,
                                "task_item": 101,
                                "candidate_answer": "Ответ кандидата 1",
                                "interviewer_comment": "Комментарий интервьюера 1",
                            },
                            {
                                "id": 2,
                                "test_task": 1,
                                "task_item": 102,
                                "candidate_answer": "Ответ кандидата 2",
                                "interviewer_comment": "Комментарий интервьюера 2",
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
        operation_summary="Создать элемент задания",
        operation_description="Создает новый элемент задания, связанный с тестовым заданием.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["test_task", "task_item", "candidate_answer"],
            properties={
                "test_task": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="ID тестового задания",
                    example=1,
                ),
                "task_item": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="ID задания", example=101
                ),
                "candidate_answer": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Ответ кандидата",
                    example="Ответ кандидата",
                ),
                "interviewer_comment": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Комментарий интервьюера",
                    example="Комментарий к ответу",
                ),
            },
        ),
        responses={
            201: openapi.Response(
                description="Элемент задания успешно создан",
                examples={
                    "application/json": {
                        "id": 3,
                        "test_task": 1,
                        "task_item": 103,
                        "candidate_answer": "Ответ кандидата 3",
                        "interviewer_comment": "Комментарий интервьюера 3",
                    }
                },
            ),
            400: "Ошибка в запросе",
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
