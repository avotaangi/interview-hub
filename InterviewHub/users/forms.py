from django import forms
from .models import Candidate


class CandidateForm(forms.ModelForm):
    additional_info = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Введите дополнительную информацию',
            'rows': 4,  # Укажите желаемое количество строк
            'cols': 40  # Укажите желаемое количество колонок
        }),
        required=False  # Сделайте поле необязательным, если это необходимо
    )

    class Meta:
        model = Candidate
        fields = ["birth_date", "city", "social_media", "additional_info"]

    def save(self, commit=True):
        # Вызываем метод save формы и получаем объект
        candidate = super().save(commit=False)

        # Устанавливаем дополнительные данные
        candidate.created_by = self.initial.get("created_by")

        # Сохраняем в базу данных, если commit=True
        if commit:
            candidate.save()

        return candidate