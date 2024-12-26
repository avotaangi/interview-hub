from datetime import timedelta

import django_filters
from django.http import Http404
from drf_yasg import openapi
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, Count, F
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.utils import timezone
from ..models import Resume, Skill, JobExperience
from ..serializers.resume_serializers import ResumeSerializer

class ResumeFilter(django_filters.FilterSet):
    min_salary = django_filters.NumberFilter(
        field_name="desired_salary", lookup_expr="gte", label="Минимальная зарплата"
    )
    max_salary = django_filters.NumberFilter(
        field_name="desired_salary", lookup_expr="lte", label="Максимальная зарплата"
    )

    class Meta:
        model = Resume
        fields = ["candidate", "desired_position", "desired_salary"]


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class ResumeViewSet(viewsets.ModelViewSet):
    """
    API для работы с резюме кандидатов.
    """

    queryset = Resume.objects.prefetch_related("skills", "job_experiences", "candidate")
    serializer_class = ResumeSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ResumeFilter
    filterset_fields = ["candidate", "desired_position"]

    @swagger_auto_schema(
        operation_summary="Получить список резюме",
        operation_description="Получить список всех резюме с поддержкой фильтров, поиска и пагинации.",
        manual_parameters=[
            openapi.Parameter(
                name="candidate",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Уникальный ID кандидата",
            ),
            openapi.Parameter(
                name="page",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Номер страницы",
            ),
            openapi.Parameter(
                name="page_size",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Количество элементов на странице",
            ),
            openapi.Parameter(
                name="desired_position",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Фильтр по желаемой должности",
            ),
            openapi.Parameter(
                name="desired_salary",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Фильтр по желаемой зарплате",
            ),
        ],
        responses={200: ResumeSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Создать новое резюме",
        operation_description="Создать новое резюме для кандидата.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["candidate", "desired_position", "desired_salary"],
            properties={
                "candidate_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="ID кандидата, которому принадлежит резюме.",
                    example=1,
                ),
                "desired_position": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Желаемая должность кандидата.",
                    example="Software Developer",
                ),
                "desired_salary": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Желаемая зарплата кандидата.",
                    example=60000,
                ),
                "skills_data": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER),
                    description="Список ID навыков, которые кандидат хочет указать.",
                    example=[1, 2, 3],
                ),
                "job_experiences_data": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER),
                    description="Список ID опыта работы, который кандидат хочет указать.",
                    example=[5, 8],
                ),
                "additional_info": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Дополнительная информация о кандидате.",
                    example="Ищу удаленную работу, готов к переезду.",
                ),
            },
        ),
        responses={
            201: openapi.Response(
                description="Резюме успешно создано",
                examples={
                    "application/json": {
                        "id": 1,
                        "candidate": 1,
                        "desired_position": "Software Developer",
                        "desired_salary": 60000.00,
                        "skills": [1, 2, 3],
                        "job_experiences": [5, 8],
                        "additional_info": "Ищу удаленную работу, готов к переезду.",
                        "created_at": "2024-01-01T10:00:00Z",
                    }
                },
            ),
            400: "Ошибка валидации",
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Получить информацию о резюме",
        operation_description="Получить информацию о конкретном резюме по его ID.",
        responses={200: ResumeSerializer, 404: "Резюме не найдено"},
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее резюме",
            ),
        ],
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Получить информацию о конкретном резюме по его ID.
        """
        pk = kwargs.get("pk")
        try:
            # Попытка получить резюме по pk
            resume = Resume.objects.get(pk=pk)
        except Resume.DoesNotExist:
            # Если объект не найден, выбрасывается Http404
            raise Http404(f"Резюме с ID {pk} не найдено.")

        # Если найдено, сериализуем и возвращаем
        serializer = self.get_serializer(resume)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Обновить резюме",
        operation_description="Полностью обновить информацию о резюме.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["candidate", "desired_position", "desired_salary"],
            properties={
                "candidate_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="ID кандидата, которому принадлежит резюме.",
                    example=1,
                ),
                "desired_position": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Желаемая должность кандидата.",
                    example="Software Developer",
                ),
                "desired_salary": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Желаемая зарплата кандидата.",
                    example=60000,
                ),
                "skills_data": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER),
                    description="Список ID навыков, которые кандидат хочет указать.",
                    example=[1, 2, 3],
                ),
                "job_experiences_data": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER),
                    description="Список ID опыта работы, который кандидат хочет указать.",
                    example=[5, 8],
                ),
                "additional_info": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Дополнительная информация о кандидате.",
                    example="Ищу удаленную работу, готов к переезду.",
                ),
            },
        ),
        responses={
            200: ResumeSerializer,
            400: "Ошибка валидации",
            404: "Резюме не найдено",
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее резюме",
            ),
        ],
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Частично обновить резюме",
        operation_description="Частично обновить информацию о резюме.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["candidate", "desired_position", "desired_salary"],
            properties={
                "candidate_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="ID кандидата, которому принадлежит резюме.",
                    example=1,
                ),
                "desired_position": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Желаемая должность кандидата.",
                    example="Software Developer",
                ),
                "desired_salary": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Желаемая зарплата кандидата.",
                    example=60000,
                ),
                "skills_data": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER),
                    description="Список ID навыков, которые кандидат хочет указать.",
                    example=[1, 2, 3],
                ),
                "job_experiences_data": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER),
                    description="Список ID опыта работы, который кандидат хочет указать.",
                    example=[5, 8],
                ),
                "additional_info": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Дополнительная информация о кандидате.",
                    example="Ищу удаленную работу, готов к переезду.",
                ),
            },
        ),
        responses={
            200: ResumeSerializer,
            400: "Ошибка валидации",
            404: "Резюме не найдено",
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее резюме",
            ),
        ],
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Удалить резюме",
        operation_description="Удалить резюме по его ID.",
        responses={204: "Резюме успешно удалено", 404: "Резюме не найдено"},
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее резюме",
            ),
        ],
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Фильтровать резюме по дате",
        operation_description="Получить резюме, созданные за указанный период (параметры 'start_date' и 'end_date'). Если параметры не указаны, будет использован период за последние 7 дней.",
        responses={200: ResumeSerializer(many=True)},
        manual_parameters=[
            openapi.Parameter(
                name="start_date",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Дата начала периода (формат: YYYY-MM-DD)",
                example="2024-11-01",
            ),
            openapi.Parameter(
                name="end_date",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Дата конца периода (формат: YYYY-MM-DD)",
                example="2024-11-07",
            ),
        ],
    )
    @action(methods=["GET"], detail=False)
    def filter_by_date(self, request):
        # Получаем параметры даты из запроса
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        # Если даты не переданы, фильтруем за последние 7 дней
        if not start_date or not end_date:
            end_date = timezone.now()
            start_date = end_date - timedelta(days=7)
        else:
            # Преобразуем строки в объекты Date
            try:
                start_date = timezone.datetime.strptime(start_date, "%Y-%m-%d").date()
                end_date = timezone.datetime.strptime(end_date, "%Y-%m-%d").date()
            except ValueError:
                return Response(
                    {"error": "Неверный формат даты. Используйте формат YYYY-MM-DD."},
                    status=400,
                )

        # Фильтруем резюме по дате создания
        resumes = self.get_queryset().filter(
            created_at__gte=start_date, created_at__lte=end_date
        )

        # Пагинация
        page = self.paginate_queryset(resumes)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # Если пагинация не используется, просто возвращаем результат
        serializer = self.get_serializer(resumes, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        method="post",
        operation_summary="Добавить навык к резюме",
        operation_description="Добавить навык к существующему резюме кандидата.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["skill_id"],
            properties={
                "skill_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    example=1,
                    description="ID навыка для добавления к резюме.",
                ),
            },
        ),
        responses={200: "Навык добавлен", 400: "Навык не найден"},
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее резюме",
            ),
        ],
    )
    @action(methods=["POST"], detail=True)
    def add_skill(self, request, pk=None):
        resume = self.get_object()
        skill_id = request.data.get("skill_id")
        try:
            skill = Skill.objects.get(id=skill_id)
            resume.skills.add(skill)
            resume.save()
            return Response({"status": "Навык добавлен"})
        except Skill.DoesNotExist:
            return Response({"error": "Навык не найден"}, status=400)

    @swagger_auto_schema(
        method="post",
        operation_summary="Удалить навык из резюме",
        operation_description="Удалить навык из существующего резюме кандидата.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["skill_id"],
            properties={
                "skill_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    example=1,
                    description="ID навыка для удаления из резюме.",
                ),
            },
        ),
        responses={
            200: "Навык удален",
            400: "Ошибка: Навык не найден или не связан с резюме",
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее резюме",
            ),
        ],
    )
    @action(methods=["POST"], detail=True)
    def remove_skill(self, request, pk=None):
        resume = self.get_object()
        skill_id = request.data.get("skill_id")
        try:
            skill = Skill.objects.get(id=skill_id)
            if skill in resume.skills.all():
                resume.skills.remove(skill)
                resume.save()
                return Response({"status": "Навык удален"})
            else:
                return Response(
                    {"error": "Навык не связан с данным резюме"}, status=400
                )
        except Skill.DoesNotExist:
            return Response({"error": "Навык не найден"}, status=400)

    @swagger_auto_schema(
        operation_summary="Добавить опыт работы к резюме",
        operation_description="Добавить опыт работы к существующему резюме кандидата.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["job_experience_id"],
            properties={
                "job_experience_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    example=1,
                    description="ID опыта работы для добавления к резюме.",
                ),
            },
        ),
        responses={200: "Опыт работы добавлен", 400: "Ошибка: Опыт работы не найден"},
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее резюме",
            ),
        ],
    )
    @action(methods=["POST"], detail=True)
    def add_job_experience(self, request, pk=None):
        resume = self.get_object()
        job_experience_id = request.data.get("job_experience_id")
        try:
            job_experience = JobExperience.objects.get(id=job_experience_id)
            resume.job_experiences.add(job_experience)
            resume.save()
            return Response({"status": "Опыт работы добавлен"})
        except JobExperience.DoesNotExist:
            return Response({"error": "Опыт работы не найден"}, status=400)

    @swagger_auto_schema(
        method="post",
        operation_summary="Удалить опыт работы из резюме",
        operation_description="Удалить опыт работы из существующего резюме кандидата.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["job_experience_id"],
            properties={
                "job_experience_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    example=1,
                    description="ID опыта работы для удаления из резюме.",
                ),
            },
        ),
        responses={
            200: "Опыт работы удален",
            400: "Ошибка: Опыт работы не найден или не связан с резюме",
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальное целое значение, идентифицирующее резюме",
            ),
        ],
    )
    @action(methods=["POST"], detail=True)
    def remove_job_experience(self, request, pk=None):
        resume = self.get_object()
        job_experience_id = request.data.get("job_experience_id")
        try:
            job_experience = JobExperience.objects.get(id=job_experience_id)
            if job_experience in resume.job_experiences.all():
                resume.job_experiences.remove(job_experience)
                resume.save()
                return Response({"status": "Опыт работы удален"})
            else:
                return Response(
                    {"error": "Опыт работы не связан с данным резюме"}, status=400
                )
        except JobExperience.DoesNotExist:
            return Response({"error": "Опыт работы не найден"}, status=400)

    @swagger_auto_schema(
        operation_summary="Фильтрация резюме по зарплате, дате публикации и опыту работы",
        operation_description="Получить резюме, удовлетворяющие условиям: зарплата не превышает желаемую и опубликованы не позднее заданного количества дней, либо имеют опыт работы более чем в указанном количестве компаний.",
        responses={200: ResumeSerializer(many=True)},
        manual_parameters=[
            openapi.Parameter(
                name="desired_salary",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Максимальная желаемая зарплата кандидата.",
                example=70000,
                required=True,
            ),
            openapi.Parameter(
                name="days_since_posted",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Максимальное количество дней с момента публикации резюме.",
                example=30,
                required=True,
            ),
            openapi.Parameter(
                name="min_job_experience_companies",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Минимальное количество компаний, в которых был опыт работы.",
                example=3,
                required=True,
            ),
        ],
    )
    @action(methods=["GET"], detail=False)
    def filter_by_salary_and_experience(self, request):
        # Получаем параметры из запроса
        desired_salary = request.query_params.get("desired_salary")
        days_since_posted = request.query_params.get("days_since_posted")
        min_job_experience_companies = request.query_params.get(
            "min_job_experience_companies"
        )

        # Получаем текущую дату
        current_date = timezone.now()

        # Формируем условия фильтрации
        filters = Q()

        if desired_salary:
            filters &= Q(desired_salary__lte=desired_salary)

        if days_since_posted:
            try:
                days_since_posted = int(days_since_posted)
                # Рассчитываем дату, на которую резюме должны быть опубликованы
                date_limit = current_date - timedelta(days=days_since_posted)
                filters &= ~Q(created_at__lt=date_limit)
            except ValueError:
                return Response(
                    {"error": "Неверный формат дня публикации."}, status=400
                )

        # Аннотируем резюме с подсчетом количества связанных записей в job_experiences
        resumes = self.get_queryset().annotate(num_companies=Count("job_experiences"))

        if min_job_experience_companies:
            try:
                min_job_experience_companies = int(min_job_experience_companies)
                filters |= Q(num_companies__gte=min_job_experience_companies)
            except ValueError:
                return Response(
                    {"error": "Неверный формат для количества компаний."}, status=400
                )

        # Применяем фильтры с учетом аннотации
        resumes = resumes.filter(filters)

        # Пагинация
        page = self.paginate_queryset(resumes)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # Если пагинация не используется, просто возвращаем результат
        serializer = self.get_serializer(resumes, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Топ-5 резюме с самой высокой зарплатой",
        operation_description="Получить первые 5 резюме, отсортированные по желаемой зарплате в порядке убывания.",
        responses={200: ResumeSerializer(many=True)},
    )
    @action(methods=["GET"], detail=False)
    def top_highest_salaries(self, request):
        """
        Возвращает топ-5 резюме с самой высокой желаемой зарплатой.
        """
        resumes = self.get_queryset().order_by("-desired_salary")[:5]
        serializer = self.get_serializer(resumes, many=True)
        return Response(serializer.data)


    @swagger_auto_schema(
        operation_summary="Фильтрация резюме по зарплатным ожиданиям",
        operation_description="Получить резюме, где желаемая зарплата превышает текущую зарплату на указанный процент.",
        manual_parameters=[
            openapi.Parameter(
                name="percentage",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Процент превышения желаемой зарплаты над текущей.",
                example=20,
                required=True,
            ),
        ],
        responses={200: ResumeSerializer(many=True)},
    )
    @action(methods=["GET"], detail=False)
    def filter_by_salary_expectation(self, request):
        """
        Возвращает резюме, где desired_salary > current_salary + (current_salary * percentage / 100).
        """
        try:
            percentage = int(request.query_params.get("percentage", 20))  # Берем процент из параметра запроса
        except ValueError:
            return Response(
                {"error": "Неверный формат процента. Укажите целое число."}, status=400
            )

        # Вычисляем фильтр с использованием F-выражений
        resumes = self.get_queryset().filter(
            desired_salary__gt=F("current_salary") + (F("current_salary") * percentage / 100)
        )

        # Пагинация
        page = self.paginate_queryset(resumes)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # Если пагинация не используется
        serializer = self.get_serializer(resumes, many=True)
        return Response(serializer.data)
