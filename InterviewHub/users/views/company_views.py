from django.core.cache import cache
from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response

from ..models import Company
from ..serializers.company_serializer import CompanySerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..models import Company
from ..serializers.company_serializer import CompanySerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class CompanyViewSet(viewsets.ModelViewSet):
    """
    API для управления компаниями.
    """

    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter]
    search_fields = ["name", "description"]

    @swagger_auto_schema(
        operation_summary="Получить список компаний",
        operation_description="Получить список всех компаний с поддержкой фильтров, поиска и пагинации.",
        manual_parameters=[
            openapi.Parameter(
                name="search",
                in_=openapi.IN_QUERY,
                description="Поиск компании по названию или описанию",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                name="page",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Номер страницы для пагинации",
                default=1
            ),
            openapi.Parameter(
                name="page_size",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Количество элементов на странице",
                default=10
            ),
        ],
        responses={
            200: openapi.Response(
                description="Успешное получение списка компаний",
                examples={
                    "application/json": {
                        "count": 2,
                        "next": None,
                        "previous": None,
                        "results": [
                            {
                                "id": 1,
                                "name": "Example Company",
                                "description": "Описание компании.",
                                "location": "Москва",
                                "established_date": "2000-01-01",
                                "logo": "https://example.com/media/company_logos/logo.png",
                            },
                            {
                                "id": 2,
                                "name": "Another Company",
                                "description": "Другая компания.",
                                "location": "Санкт-Петербург",
                                "established_date": "1995-01-01",
                                "logo": None,
                            },
                        ],
                    }
                },
            )
        },
    )
    def list(self, request, *args, **kwargs):
        """
        Получить список компаний с поддержкой кэширования.
        """
        # Создаём ключ для кэша на основе параметров запроса
        cache_key = f"companies_{request.query_params.urlencode()}"
        cached_data = cache.get(cache_key)

        if cached_data:
            # Возвращаем кэшированные данные
            return Response(cached_data)

        # Получаем данные через стандартный метод
        response = super().list(request, *args, **kwargs)

        # Сохраняем данные в кэш на 15 минут
        cache.set(cache_key, response.data, timeout=60 * 15)

        return response

    @swagger_auto_schema(
        operation_summary="Создать новую компанию",
        operation_description="Создать запись новой компании с указанием названия, описания, местоположения, даты основания и логотипа.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["name", "location"],
            properties={
                "name": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example="Example Company",
                    description="Название компании.",
                ),
                "description": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example="Это пример описания компании.",
                    description="Описание компании.",
                ),
                "location": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example="Москва",
                    description="Местоположение компании.",
                ),
                "established_date": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format="date",
                    example="2000-01-01",
                    description="Дата основания компании в формате YYYY-MM-DD.",
                ),
                "logo": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format="binary",
                    description="Файл изображения логотипа компании.",
                ),
            },
        ),
        responses={
            201: openapi.Response(
                description="Компания успешно создана",
                examples={
                    "application/json": {
                        "id": 1,
                        "name": "Example Company",
                        "description": "Описание компании.",
                        "location": "Москва",
                        "established_date": "2000-01-01",
                        "logo": "https://example.com/media/company_logos/logo.png",
                    }
                },
            ),
            400: "Неверный запрос",
        },
    )
    def create(self, request, *args, **kwargs):
        """
        Создание компании и очистка кэша списка компаний.
        """
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            cache.delete_pattern("companies_*")
        return response


    @swagger_auto_schema(
        operation_summary="Получить информацию о компании",
        operation_description="Получить информацию о конкретной компании по её ID.",
        responses={200: CompanySerializer, 404: "Компания не найдена"},
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее компанию",
            ),
        ],
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Получение информации о компании с поддержкой кэширования.
        """
        # Получаем ID компании из параметров
        company_id = kwargs.get("pk")

        # Формируем ключ для кэша
        cache_key = f"company_{company_id}"

        # Проверяем, есть ли данные в кэше
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        # Если данных нет в кэше, получаем через стандартный метод
        try:
            response = super().retrieve(request, *args, **kwargs)
            return response
        except Exception:
            return Response({"detail": "Компания не найдена"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary="Обновить информацию о компании",
        operation_description="Полностью обновить запись компании.",
        request_body=CompanySerializer,
        responses={
            200: CompanySerializer,
            400: "Неверный запрос",
            404: "Компания не найдена",
        },
    )
    def update(self, request, *args, **kwargs):
        """
        Обновление компании и очистка кэша.
        """
        company_id = kwargs.get("pk")
        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            cache.delete_pattern("companies_*")
            cache.delete(f"company_{company_id}")
        return response

    @swagger_auto_schema(
        operation_summary="Частично обновить информацию о компании",
        operation_description="Частично обновить данные компании.",
        request_body=CompanySerializer,
        responses={
            200: CompanySerializer,
            400: "Неверный запрос",
            404: "Компания не найдена",
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее компанию",
            ),
        ],
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Частичное обновление компании и очистка кэша.
        """
        company_id = kwargs.get("pk")
        response = super().partial_update(request, *args, **kwargs)
        if response.status_code == 200:
            cache.delete_pattern("companies_*")
            cache.delete(f"company_{company_id}")
        return response

    @swagger_auto_schema(
        operation_summary="Удалить компанию",
        operation_description="Удалить запись компании по её ID.",
        responses={204: "Компания успешно удалена", 404: "Компания не найдена"},
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее компанию",
            ),
        ],
    )
    def destroy(self, request, *args, **kwargs):
        """
        Удаление компании и очистка кэша, связанного с компаниями.
        """
        # Получаем ID удаляемой компании
        instance_id = kwargs.get("pk")

        # Удаляем запись через стандартный метод
        response = super().destroy(request, *args, **kwargs)

        if response.status_code == 204:  # Удаление прошло успешно
            # Удаляем кэш, связанный со списком компаний
            cache_key_pattern = "companies_"
            for key in cache.keys(f"{cache_key_pattern}*"):
                cache.delete(key)

            # Удаляем кэш, связанный с конкретной компанией (если используется)
            specific_cache_key = f"company_{instance_id}"
            cache.delete(specific_cache_key)

        return response
