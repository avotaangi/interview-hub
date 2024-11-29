from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import RegisterSerializer, UserSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import RegisterSerializer


class RegisterView(APIView):
    @swagger_auto_schema(
        operation_summary="Регистрация пользователя",
        operation_description=(
                "Эндпоинт для регистрации нового пользователя. "
                "Требуется указать имя пользователя (username), email, пароль, телефон, аватар, имя, фамилию и пол."
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Имя пользователя (уникальное)'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Электронная почта (уникальная)'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Пароль'),
                'password_confirm': openapi.Schema(type=openapi.TYPE_STRING, description='Подтверждение пароля'),
                'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Телефон (уникальный)'),
                'avatar': openapi.Schema(type=openapi.TYPE_FILE, description='Изображение аватара (необязательно)'),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='Имя'),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Фамилия'),
                'gender': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['Мужской', 'Женский'],
                    description='Пол'
                ),
            },
            required=['username', 'email', 'password', 'password_confirm'],
        ),
        responses={
            201: openapi.Response(description="Пользователь успешно зарегистрирован."),
            400: openapi.Response(description="Ошибка валидации данных."),
        }
    )
    def post(self, request):
        """
        Регистрация нового пользователя.
        """
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Пользователь успешно зарегистрирован."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    Кастомный эндпоинт для логина по email, username или phone.
    """

    @swagger_auto_schema(
        operation_summary="Логин пользователя",
        operation_description=(
                "Эндпоинт для авторизации. Можно использовать email, username или phone в качестве логина, "
                "а также пароль для аутентификации."
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'login': openapi.Schema(type=openapi.TYPE_STRING, description='Email, username или номер телефона'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Пароль'),
            },
            required=['login', 'password'],
        ),
        responses={
            200: openapi.Response(
                description="Авторизация успешна",
                examples={
                    'application/json': {
                        "refresh": "string",
                        "access": "string",
                    }
                }
            ),
            401: openapi.Response(description="Неверные учетные данные.")
        }
    )
    def post(self, request):
        login = request.data.get('login')
        password = request.data.get('password')

        if not login or not password:
            return Response(
                {"detail": "Необходимо указать логин и пароль."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Попытка найти пользователя по login (email, username или phone)

        user = authenticate(request, username=login, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {"detail": "Неверные учетные данные."},
            status=status.HTTP_401_UNAUTHORIZED
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Выход из системы",
        operation_description="Позволяет пользователю выйти из системы, делая его refresh-токен недействительным.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "refresh": openapi.Schema(type=openapi.TYPE_STRING, description="Refresh-токен")
            },
            required=["refresh"],
        ),
        responses={
            205: openapi.Response(description="Выход выполнен успешно."),
            400: openapi.Response(description="Ошибка в запросе."),
        }
    )
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # Этот метод теперь работает
            return Response({"message": "Вы успешно вышли из системы."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CurrentUserView(APIView):
    """
    Эндпоинт для получения информации о текущем пользователе.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Получение данных текущего пользователя",
        operation_description="Эндпоинт возвращает информацию о текущем авторизованном пользователе.",
        responses={
            200: openapi.Response(
                description="Успешный ответ с данными пользователя.",
                schema=UserSerializer
            ),
            401: openapi.Response(
                description="Неавторизованный доступ.",
                examples={"application/json": {"detail": "Учетные данные не были предоставлены."}}
            ),
        },
    )
    def get(self, request):
        """
        Возвращает данные текущего авторизованного пользователя.
        """
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)
