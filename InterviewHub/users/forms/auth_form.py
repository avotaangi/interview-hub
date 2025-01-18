import logging

from django import forms
from django.contrib.auth.forms import AuthenticationForm

from ..models import User, Candidate, Interviewer

import logging

logger = logging.getLogger(__name__)


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Пароль",
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput,
        label="Подтверждение пароля",
    )
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={
            "placeholder": "Введите имя пользователя"
        })
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            "placeholder": "Введите email"
        })
    )
    user_type = forms.ChoiceField(
        choices=[('candidate', 'Кандидат'), ('interviewer', 'Интервьюер')],
        widget=forms.HiddenInput(),  # Скрытое поле
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            self.add_error('password_confirm', 'Пароли не совпадают.')
        return cleaned_data

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Логин",
        widget=forms.TextInput(attrs={
            "placeholder": "Введите ваш логин"
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Введите ваш пароль"
        }),
        label="Пароль"
    )
