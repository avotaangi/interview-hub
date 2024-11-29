from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from .models import User


class CustomAuthBackend(ModelBackend):
    """
    Кастомный бэкэнд аутентификации, поддерживающий вход по email, phone или username.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Метод аутентификации.
        :param request: HTTP-запрос
        :param username: Логин пользователя (email, phone или username)
        :param password: Пароль пользователя
        :param kwargs: Дополнительные параметры
        :return: User или None
        """
        if not username or not password:
            return None

        try:
            # Ищем пользователя по email, phone или username
            user = User.objects.filter(
                Q(email=username) | Q(phone=username) | Q(username=username)
            ).first()

            # Проверяем пароль, если пользователь найден
            if user and user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

        return None

    def get_user(self, user_id):
        """
        Получение пользователя по ID.
        :param user_id: ID пользователя
        :return: User или None
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
