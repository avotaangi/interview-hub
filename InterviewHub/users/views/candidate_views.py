from django.core.cache import cache
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from ..models import Candidate, CandidateForm
from ..serializers.candidate_serializer import CandidateSerializer
from django.shortcuts import get_object_or_404


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class CandidateViewSet(viewsets.ModelViewSet):
    """
    API для управления кандидатами.
    """

    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["user__email", "city"]

    @swagger_auto_schema(
        operation_summary="Получить список кандидатов",
        operation_description="Получить список всех кандидатов с поддержкой фильтров, поиска и пагинации.",
        responses={
            200: openapi.Response(
                description="Успешное получение списка кандидатов",
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
                                    "email": "example@example.com",
                                    "first_name": "Иван",
                                    "last_name": "Иванов",
                                },
                                "birth_date": "1990-01-01",
                                "city": "Москва",
                                "social_media": "https://vk.ru/profile",
                            }
                        ],
                    }
                },
            )
        },
        manual_parameters=[
            openapi.Parameter(
                name="user__email",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Электронная почта пользователя для фильтрации кандидатов"
            ),
            openapi.Parameter(
                name="city",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Город для фильтрации кандидатов"
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
    )
    def list(self, request, *args, **kwargs):
        """
        Получить список кандидатов с поддержкой кэширования.
        """
        # Генерация ключа для кэша с учётом параметров запроса
        cache_key = f"candidates_{request.query_params}"
        cached_response = cache.get(cache_key)

        if cached_response is not None:
            return Response(cached_response)

        # Получение данных через стандартный метод
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60 * 15)  # Кэш на 15 минут
        return response

    @swagger_auto_schema(
        operation_summary="Создать нового кандидата",
        operation_description="Создать запись нового кандидата с информацией о пользователе, дате рождения, городе и соцсетях.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["user", "city"],
            properties={
                "user_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    example=1,
                    description="ID пользователя, связанного с кандидатом.",
                ),
                "birth_date": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format="date",
                    example="1990-01-01",
                    description="Дата рождения кандидата в формате YYYY-MM-DD.",
                ),
                "city": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example="Москва",
                    description="Город проживания кандидата.",
                ),
                "social_media": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example="https://linkedin.com/in/example",
                    description="Ссылка на социальные сети кандидата.",
                ),
            },
        ),
        responses={
            201: openapi.Response(
                description="Кандидат успешно создан",
                examples={
                    "application/json": {
                        "id": 1,
                        "user": 1,
                        "birth_date": "1990-01-01",
                        "city": "Москва",
                        "social_media": "https://linkedin.com/in/example",
                    }
                },
            ),
            400: "Неверный запрос",
        },
    )
    def create(self, request, *args, **kwargs):
        """
        Создать кандидата с использованием Django формы и очистить кэш списка.
        """

        form = CandidateForm(data=request.data)

        if form.is_valid():  # Проверяем корректность формы
            cleaned_data = form.cleaned_data  # Получаем очищенные данные формы
            candidate = form.save(commit=False)  # Создаем объект, но не сохраняем его
            candidate.save()  # Сохраняем объект в базе данных

            cache.delete_pattern("candidates_*")  # Удаляем кэш
            return Response(
                {"detail": "Кандидат успешно создан.", "data": cleaned_data},
                status=201,
            )
        return Response(
            {"detail": "Ошибка валидации формы.", "errors": form.errors},
            status=400,
        )

    @swagger_auto_schema(
        operation_summary="Получить информацию о кандидате",
        operation_description="Получить информацию о конкретном кандидате по его ID.",
        responses={200: CandidateSerializer, 404: "Кандидат не найден"},
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее кандидата",
            ),
        ],
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Получить информацию о кандидате с поддержкой кэширования.
        """
        candidate_id = kwargs.get("pk")
        cache_key = f"candidate_{candidate_id}"

        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        response = super().retrieve(request, *args, **kwargs)
        if response.status_code == 200:
            cache.set(cache_key, response.data, timeout=60 * 15)
        return response

    @swagger_auto_schema(
        operation_summary="Обновить информацию о кандидате",
        operation_description="Полностью обновить запись кандидата.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["user", "city"],
            properties={
                "user_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    example=1,
                    description="ID пользователя, связанного с кандидатом.",
                ),
                "birth_date": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format="date",
                    example="1990-01-01",
                    description="Дата рождения кандидата в формате YYYY-MM-DD.",
                ),
                "city": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example="Москва",
                    description="Город проживания кандидата.",
                ),
                "social_media": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example="https://linkedin.com/in/example",
                    description="Ссылка на социальные сети кандидата.",
                ),
            },
        ),
        responses={
            200: CandidateSerializer,
            400: "Неверный запрос",
            404: "Кандидат не найден",
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее кандидата",
            ),
        ],
    )
    def update(self, request, *args, **kwargs):
        """
        Полностью обновить информацию о кандидате и очистить кэш.
        """
        candidate_id = kwargs.get("pk")
        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            cache.delete_pattern("candidates_*")
            cache.delete(f"candidate_{candidate_id}")
        return response

    @swagger_auto_schema(
        operation_summary="Частично обновить информацию о кандидате",
        operation_description="Частично обновить данные кандидата.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["user", "city"],
            properties={
                "user_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    example=1,
                    description="ID пользователя, связанного с кандидатом.",
                ),
                "birth_date": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format="date",
                    example="1990-01-01",
                    description="Дата рождения кандидата в формате YYYY-MM-DD.",
                ),
                "city": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example="Москва",
                    description="Город проживания кандидата.",
                ),
                "social_media": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example="https://linkedin.com/in/example",
                    description="Ссылка на социальные сети кандидата.",
                ),
            },
        ),
        responses={
            200: CandidateSerializer,
            400: "Неверный запрос",
            404: "Кандидат не найден",
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее кандидата",
            ),
        ],
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Частично обновить информацию о кандидате и очистить кэш.
        """
        candidate_id = kwargs.get("pk")
        response = super().partial_update(request, *args, **kwargs)
        if response.status_code == 200:
            cache.delete_pattern("candidates_*")
            cache.delete(f"candidate_{candidate_id}")
        return response

    @swagger_auto_schema(
        operation_summary="Удалить кандидата",
        operation_description="Удалить запись кандидата по его ID.",
        responses={204: "Кандидат успешно удален", 404: "Кандидат не найден"},
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее кандидата",
            ),
        ],
    )
    def destroy(self, request, *args, **kwargs):
        """
        Удалить кандидата и очистить кэш.
        """
        candidate_id = kwargs.get("pk")
        response = super().destroy(request, *args, **kwargs)
        if response.status_code == 204:
            cache.delete_pattern("candidates_*")
            cache.delete(f"candidate_{candidate_id}")
        return response

    @swagger_auto_schema(
        operation_summary="Подсчитать кандидатов из города",
        operation_description="Возвращает количество кандидатов, связанных с указанным городом.",
        manual_parameters=[
            openapi.Parameter(
                name="city",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Название города для подсчёта кандидатов",
            ),
        ],
        responses={
            200: openapi.Response(
                description="Успешный подсчёт кандидатов",
                examples={
                    "application/json": {
                        "city": "Москва",
                        "candidate_count": 10,
                    }
                },
            ),
            404: "Город не найден",
        },
    )
    @action(detail=False, methods=["get"], url_path="count-by-city")
    def count_by_city(self, request, *args, **kwargs):
        """
        Подсчитать количество кандидатов из указанного города.
        """
        city = request.query_params.get("city")
        if not city:
            return Response(
                {"detail": "Параметр 'city' обязателен для выполнения запроса."},
                status=400,
            )

        # Проверяем, существует ли хотя бы один кандидат в указанном городе
        candidate = get_object_or_404(Candidate, city=city)

        # Подсчитываем количество кандидатов
        candidate_count = Candidate.objects.filter(city=city).count()

        return Response({"city": city, "candidate_count": candidate_count})






