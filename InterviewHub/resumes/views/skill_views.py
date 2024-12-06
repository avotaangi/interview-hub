from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..models import Skill
from ..serializers.skill_serializers import SkillSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name', 'description']

    @swagger_auto_schema(
        operation_summary="Получить список навыков",
        operation_description="Возвращает список навыков с возможностью фильтрации и поиска.",
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
                                    "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID навыка"),
                                    "name": openapi.Schema(type=openapi.TYPE_STRING, description="Название навыка"),
                                    "description": openapi.Schema(type=openapi.TYPE_STRING, description="Описание навыка")
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
                name="name",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Поиск по названию навыка"
            ),
            openapi.Parameter(
                name="search",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Поиск по описанию навыка"
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
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Создать новый навык",
        operation_description="Создает новый навык на основе переданных данных.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["name"],
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING, description="Название навыка", example="Python"),
                "description": openapi.Schema(type=openapi.TYPE_STRING, description="Описание навыка", example="Программирование на Python."),
            }
        ),
        responses={
            201: openapi.Response(
                description="Навык успешно создан",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID навыка"),
                        "name": openapi.Schema(type=openapi.TYPE_STRING, description="Название навыка"),
                        "description": openapi.Schema(type=openapi.TYPE_STRING, description="Описание навыка")
                    }
                )
            ),
            400: "Ошибка в запросе"
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Получить навык по ID",
        operation_description="Возвращает данные о навыке по указанному ID.",
        responses={
            200: openapi.Response(
                description="Успешный ответ",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID навыка"),
                        "name": openapi.Schema(type=openapi.TYPE_STRING, description="Название навыка"),
                        "description": openapi.Schema(type=openapi.TYPE_STRING, description="Описание навыка")
                    }
                )
            ),
            404: "Навык не найден"
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее навык"
            ),
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Обновить навык",
        operation_description="Обновляет существующий навык по ID.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["name"],
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING, description="Название навыка", example="Django"),
                "description": openapi.Schema(type=openapi.TYPE_STRING, description="Описание навыка", example="Веб-фреймворк на Python."),
            }
        ),
        responses={
            200: openapi.Response(
                description="Навык успешно обновлен",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID навыка"),
                        "name": openapi.Schema(type=openapi.TYPE_STRING, description="Название навыка"),
                        "description": openapi.Schema(type=openapi.TYPE_STRING, description="Описание навыка")
                    }
                )
            ),
            400: "Ошибка в запросе",
            404: "Навык не найден"
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее навык"
            ),
        ]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Частичное обновление навыка",
        operation_description="Обновляет только указанные поля навыка по ID.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING, description="Название навыка", example="FastAPI"),
                "description": openapi.Schema(type=openapi.TYPE_STRING, description="Описание навыка",
                                           example="Асинхронный веб-фреймворк."),
            }
        ),
        responses={
            200: openapi.Response(
                description="Навык успешно обновлен (частично)",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID навыка"),
                        "name": openapi.Schema(type=openapi.TYPE_STRING, description="Название навыка"),
                        "description": openapi.Schema(type=openapi.TYPE_STRING, description="Описание навыка")
                    }
                )
            ),
            400: "Ошибка в запросе",
            404: "Навык не найден"
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее навык"
            ),
        ]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Удалить навык",
        operation_description="Удаляет навык по указанному ID.",
        responses={
            204: "Навык успешно удален",
            404: "Навык не найден"
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее навык"
            ),
        ]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
