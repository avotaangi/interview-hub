from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from ..models import Interviewer
from ..serializers.inteview_serializer import InterviewerSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..models import Interviewer
from ..serializers import InterviewerSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class InterviewerViewSet(viewsets.ModelViewSet):
    """
    API для управления интервьюерами.
    """
    queryset = Interviewer.objects.all()
    serializer_class = InterviewerSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['company', 'position', 'user__email']
    search_fields = ['user__first_name', 'user__email', 'position']

    @swagger_auto_schema(
        operation_summary="Получить список интервьюеров",
        operation_description="Получить список всех интервьюеров с поддержкой фильтров, поиска и пагинации.",
        manual_parameters=[
            openapi.Parameter(
                name='page',
                in_=openapi.IN_QUERY,
                description='Номер страницы',
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name='page_size',
                in_=openapi.IN_QUERY,
                description='Количество элементов на странице',
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name='search',
                in_=openapi.IN_QUERY,
                description='Поиск по имени, email пользователя или должности.',
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                name='company',
                in_=openapi.IN_QUERY,
                description='Фильтр по ID компании.',
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name='position',
                in_=openapi.IN_QUERY,
                description='Фильтр по должности.',
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                name='user__email',
                in_=openapi.IN_QUERY,
                description='Фильтр по email пользователя.',
                type=openapi.TYPE_STRING
            ),
        ],
        responses={
            200: openapi.Response(
                description="Успешное получение списка интервьюеров",
                examples={
                    "application/json": {
                        "count": 1,
                        "next": None,
                        "previous": None,
                        "results": [
                            {
                                "id": 1,
                                "user": {
                                    "id": 1,
                                    "name": "Иван Иванов",
                                    "email": "ivan@example.com"
                                },
                                "company": {
                                    "id": 2,
                                    "name": "Example Company"
                                },
                                "position": "Senior Developer"
                            }
                        ]
                    }
                }
            )
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Создать нового интервьюера",
        operation_description="Создать запись нового интервьюера с указанием пользователя, компании и должности.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['user', 'company', 'position'],
            properties={
                'user': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    example=1,
                    description="ID пользователя, связанного с интервьюером."
                ),
                'company': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    example=2,
                    description="ID компании, в которой работает интервьюер."
                ),
                'position': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example="Senior Developer",
                    description="Должность интервьюера."
                ),
            }
        ),
        responses={
            201: openapi.Response(
                description="Интервьюер успешно создан",
                examples={
                    "application/json": {
                        "id": 1,
                        "user": 1,
                        "company": 2,
                        "position": "Senior Developer"
                    }
                }
            ),
            400: "Неверный запрос"
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Получить информацию об интервьюере",
        operation_description="Получить информацию о конкретном интервьюере по его ID.",
        responses={
            200: InterviewerSerializer,
            404: "Интервьюер не найден"
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее интервьюера"
            ),
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Обновить информацию об интервьюере",
        operation_description="Полностью обновить запись интервьюера.",
        request_body=InterviewerSerializer,
        responses={
            200: InterviewerSerializer,
            400: "Неверный запрос",
            404: "Интервьюер не найден"
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее интервьюера"
            ),
        ]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Частично обновить информацию об интервьюере",
        operation_description="Частично обновить данные интервьюера.",
        request_body=InterviewerSerializer,
        responses={
            200: InterviewerSerializer,
            400: "Неверный запрос",
            404: "Интервьюер не найден"
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее интервьюера"
            ),
        ]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Удалить интервьюера",
        operation_description="Удалить запись интервьюера по его ID.",
        responses={
            204: "Интервьюер успешно удален",
            404: "Интервьюер не найден"
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее интервьюера"
            ),
        ]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
