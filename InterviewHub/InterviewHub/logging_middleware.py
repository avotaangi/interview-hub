import logging
import json
from datetime import datetime
import redis

from rest_framework_simplejwt.authentication import JWTAuthentication

logger = logging.getLogger('user_activity')


class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_authenticator = JWTAuthentication()
        self.redis_client = redis.StrictRedis(host='redis', port=6379, db=0)  # Настройка Redis

    def __call__(self, request):
        try:
            # Аутентифицируем пользователя вручную
            token = request.headers.get('Authorization', '').split()[1]
            validated_token = self.jwt_authenticator.get_validated_token(token)
            user = self.jwt_authenticator.get_user(validated_token)
            user_info = f"{user.first_name} {user.last_name} ({user})"
        except Exception:
            user_info = "Анонимус"

        visit_data = {
            "user": user_info,
            "path": request.path,
            "method": request.method,
            "timestamp": datetime.now().isoformat(),
        }

        # Запись данных в Redis
        self.redis_client.lpush("user_activity", json.dumps(visit_data))
        logger.info(f"Записано в Redis: {visit_data}")

        response = self.get_response(request)
        return response
