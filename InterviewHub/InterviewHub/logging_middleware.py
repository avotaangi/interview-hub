import logging

from rest_framework_simplejwt.authentication import JWTAuthentication

logger = logging.getLogger('user_activity')


class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_authenticator = JWTAuthentication()

    def __call__(self, request):
        try:
            # Аутентифицируем пользователя вручную
            validated_token = self.jwt_authenticator.get_validated_token(
                request.headers.get('Authorization').split()[1])
            user = self.jwt_authenticator.get_user(validated_token)
            logger.info(f"Пользователь: {user.first_name} {user.last_name} ({user}), Путь: {request.path}, Метод: {request.method}")

        except Exception:
            user = "Анонимус"
            logger.info(f"Пользователь: {user}, Путь: {request.path}, Метод: {request.method}")

        response = self.get_response(request)
        return response
