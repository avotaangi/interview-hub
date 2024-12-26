from django.http import HttpResponseRedirect
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import authenticate
from ..serializers.auth_serializer import RegisterSerializer


class AuthViewSet(ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=["post"])
    @swagger_auto_schema(
        operation_summary="Регистрация пользователя",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Имя пользователя (уникальное)",
                ),
                "email": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Электронная почта (уникальная)",
                ),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Пароль"
                ),
                "password_confirm": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Подтверждение пароля"
                ),
                "phone": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Телефон (уникальный)"
                ),
                "avatar": openapi.Schema(
                    type=openapi.TYPE_FILE,
                    description="Изображение аватара (необязательно)",
                ),
                "first_name": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Имя"
                ),
                "last_name": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Фамилия"
                ),
                "gender": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=["Мужской", "Женский"],
                    description="Пол",
                ),
            },
            required=["username", "email", "password", "password_confirm"],
        ),
        responses={
            201: openapi.Response(description="Пользователь успешно зарегистрирован."),
            400: openapi.Response(description="Ошибка валидации данных."),
        },
    )
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Сохранение данных в сеанс
            request.session["user_id"] = user.id
            return Response(
                {"message": "Пользователь успешно зарегистрирован."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"])
    @swagger_auto_schema(
        operation_summary="Логин пользователя",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "login": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Email, username или номер телефона",
                ),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Пароль"
                ),
            },
            required=["login", "password"],
        ),
        responses={
            200: openapi.Response(
                description="Авторизация успешна",
                examples={
                    "application/json": {
                        "refresh": "string",
                        "access": "string",
                    }
                },
            ),
            401: openapi.Response(description="Неверные учетные данные."),
        },
    )
    def login(self, request):
        login = request.data.get("login")
        password = request.data.get("password")

        if not login or not password:
            return Response(
                {"detail": "Необходимо указать логин и пароль."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(request, username=login, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            # Сохранение данных в сеанс
            request.session["user_id"] = user.id
            request.session["access_token"] = str(refresh.access_token)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {"detail": "Неверные учетные данные."}, status=status.HTTP_401_UNAUTHORIZED
        )

    @action(detail=False, methods=["post"])
    @swagger_auto_schema(
        operation_summary="Выход из системы",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "refresh": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Refresh-токен"
                )
            },
            required=["refresh"],
        ),
        responses={
            205: openapi.Response(description="Выход выполнен успешно."),
            400: openapi.Response(description="Ошибка в запросе."),
        },
    )
    def logout(self, request):
        try:
            # Очистка сеанса
            request.session.flush()
            # Перенаправление на страницу входа после выхода
            return HttpResponseRedirect(redirect_to="/login/")
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
