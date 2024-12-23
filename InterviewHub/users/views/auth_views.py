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
            serializer.save()
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

    @action(detail=False, methods=["get"])
    @swagger_auto_schema(
        operation_summary="Ссылка для авторизации через VK",
        responses={
            200: openapi.Response(
                description="Ссылка для авторизации через VK",
                examples={
                    "application/json": {
                        "vk": "https://oauth.vk.com/authorize?client_id=...&redirect_uri=...&response_type=code"
                    }
                },
            )
        },
    )
    def vk_auth_link(self, request):
        base_url = request.build_absolute_uri("/")
        vk_link = f"{base_url}accounts/vk/login/"
        return Response({"vk": vk_link}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    @swagger_auto_schema(
        operation_summary="Обновление токенов",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "refresh": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Refresh-токен для обновления токенов",
                )
            },
            required=["refresh"],
        ),
        responses={
            200: openapi.Response(
                description="Токен успешно обновлен.",
                examples={"application/json": {"access": "string"}},
            ),
            401: openapi.Response(description="Невалидный или истекший refresh-токен."),
        },
    )
    def refresh(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                {"detail": "Не указан refresh-токен."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            refresh = RefreshToken(refresh_token)
            new_access = refresh.access_token
            return Response({"access": str(new_access)}, status=status.HTTP_200_OK)
        except TokenError as e:
            return Response(
                {"detail": "Невалидный или истекший refresh-токен.", "error": str(e)},
                status=status.HTTP_401_UNAUTHORIZED,
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
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"message": "Вы успешно вышли из системы."},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
