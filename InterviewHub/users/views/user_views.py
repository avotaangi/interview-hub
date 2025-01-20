from drf_yasg import openapi
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema

from ..models import Candidate, Interviewer
from ..serializers.candidate_serializer import CandidateSerializer
from ..serializers.user_serializer import UserSerializer
from ..serializers.inteview_serializer import InterviewerSerializer


class UserViewSet(ViewSet):
    """
    ViewSet для работы с текущим пользователем.
    """

    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"])
    @swagger_auto_schema(
        operation_summary="Получение данных текущего пользователя",
        operation_description="Эндпоинт возвращает информацию о текущем авторизованном пользователе.",
        responses={
            200: openapi.Response(
                description="Успешный ответ с данными пользователя.",
                schema=UserSerializer,
            ),
            401: openapi.Response(
                description="Неавторизованный доступ.",
                examples={
                    "application/json": {
                        "detail": "Учетные данные не были предоставлены."
                    }
                },
            ),
        },
    )
    def current_user(self, request):
        """
        Возвращает данные текущего авторизованного пользователя.
        """
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)

    @action(detail=False, methods=["patch"])
    @swagger_auto_schema(
        operation_summary="Обновление данных текущего пользователя",
        operation_description="Эндпоинт позволяет обновить данные текущего пользователя (например, имя, email).",
        request_body=UserSerializer,
        responses={
            200: openapi.Response(
                description="Данные пользователя успешно обновлены.",
                schema=UserSerializer,
            ),
            400: openapi.Response(
                description="Ошибка валидации данных.",
                examples={"application/json": {"email": ["Неверный формат email."]}},
            ),
        },
    )
    def update_profile(self, request):
        """
        Обновляет данные текущего пользователя.
        """
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    @action(detail=True, methods=["get"], url_path="user-data")
    @swagger_auto_schema(
        operation_summary="Получение интервью или кандидата по user_id",
        operation_description="Эндпоинт возвращает данные интервью, кандидата или пустые значения, если ничего не найдено.",
        responses={
            200: openapi.Response(
                description="Данные успешно найдены.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "interview": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            description="Информация об интервью",
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "start_time": openapi.Schema(type=openapi.TYPE_STRING),
                                "end_time": openapi.Schema(type=openapi.TYPE_STRING),
                            },
                        ),
                        "candidate": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            description="Информация о кандидате",
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "full_name": openapi.Schema(type=openapi.TYPE_STRING),
                                "email": openapi.Schema(type=openapi.TYPE_STRING),
                            },
                        ),
                    },
                ),
            ),
            404: openapi.Response(description="Пользователь не найден."),
        },
    )
    def user_data(self, request, pk=None):
        """
        Возвращает интервью или кандидата для указанного user_id.
        """
        try:
            # Проверяем наличие пользователя
            user_id = pk
            interview = Interviewer.objects.filter(user_id=user_id).first()

            # Поиск кандидата, связанного с данным пользователем
            candidate = Candidate.objects.filter(user_id=user_id).first()

            # Подготавливаем данные для ответа
            interview_data = InterviewerSerializer(interview).data if interview else None
            candidate_data = CandidateSerializer(candidate).data if candidate else None

            response_data = {
                "interview": interview_data,
                "candidate": candidate_data,
            }

            return Response(response_data, status=200)

        except Exception as e:
            return Response(
                {"detail": f"Ошибка: {str(e)}"}, status=400
            )

