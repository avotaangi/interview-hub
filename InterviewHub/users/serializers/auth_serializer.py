from rest_framework import serializers
from ..models import User
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'phone', 'avatar', 'first_name', 'last_name',
                  'gender']

    def validate(self, attrs):
        # Проверка уникальности username
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({"username": "Имя пользователя уже занято."})

        # Проверка уникальности email
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "Пользователь с такой электронной почтой уже существует."})

        # Проверка уникальности телефона
        if attrs.get('phone') and User.objects.filter(phone=attrs['phone']).exists():
            raise serializers.ValidationError({"phone": "Пользователь с таким номером телефона уже существует."})

        # Проверка совпадения паролей
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Пароли не совпадают."})

        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone=validated_data.get('phone'),
            avatar=validated_data.get('avatar'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            gender=validated_data.get('gender'),
        )
        return user
