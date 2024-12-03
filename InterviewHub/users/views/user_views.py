from drf_yasg import openapi
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from ..serializers import UserSerializer


class UserViewSet(ViewSet):
    """
    ViewSet для работы с текущим пользователем.
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
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
    def current_user(self, request):
        """
        Возвращает данные текущего авторизованного пользователя.
        """
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)

    @action(detail=False, methods=['patch'])
    @swagger_auto_schema(
        operation_summary="Обновление данных текущего пользователя",
        operation_description="Эндпоинт позволяет обновить данные текущего пользователя (например, имя, email).",
        request_body=UserSerializer,
        responses={
            200: openapi.Response(
                description="Данные пользователя успешно обновлены.",
                schema=UserSerializer
            ),
            400: openapi.Response(
                description="Ошибка валидации данных.",
                examples={"application/json": {"email": ["Неверный формат email."]}}
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
