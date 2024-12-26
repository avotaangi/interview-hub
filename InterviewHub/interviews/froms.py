from django import forms
from .models import Interview


class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = [
            "selection",
            "start_time",
            "end_time",
            "type",
            "status",
            "feedback",
            "notes",
            "hard_skills_rate",
            "soft_skills_rate",
            "result",
            "recording_url",
            "file",
            "additional_url",
        ]
        # Или используйте exclude, чтобы указать исключения
        # exclude = ['duration', 'history']

        widgets = {
            "start_time": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "end_time": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "type": forms.TextInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "feedback": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "hard_skills_rate": forms.NumberInput(attrs={"class": "form-control"}),
            "soft_skills_rate": forms.NumberInput(attrs={"class": "form-control"}),
            "result": forms.Select(attrs={"class": "form-select"}),
            "recording_url": forms.URLInput(attrs={"class": "form-control"}),
            "file": forms.FileInput(attrs={"class": "form-control"}),
            "additional_url": forms.URLInput(attrs={"class": "form-control"}),
        }

        labels = {
            "selection": "Выбор компании",
            "start_time": "Начало интервью",
            "end_time": "Окончание интервью",
            "type": "Формат интервью",
            "status": "Текущий статус",
            "feedback": "Обратная связь по интервью",
            "notes": "Примечания",
            "hard_skills_rate": "Оценка технических навыков",
            "soft_skills_rate": "Оценка коммуникативных навыков",
            "result": "Итоговый результат",
            "recording_url": "Ссылка на запись",
            "file": "Загрузить файл",
            "additional_url": "Дополнительная ссылка",
        }

        help_texts = {
            "start_time": "Укажите дату и время начала интервью.",
            "end_time": "Укажите дату и время завершения интервью.",
            "hard_skills_rate": "Оцените технические навыки кандидата по шкале от 1 до 10.",
            "soft_skills_rate": "Оцените коммуникативные навыки кандидата по шкале от 1 до 10.",
        }

        error_messages = {
            "start_time": {
                "invalid": "Укажите корректную дату и время начала интервью.",
            },
            "end_time": {
                "invalid": "Укажите корректную дату и время окончания интервью.",
            },
            "type": {
                "max_length": "Тип интервью не может содержать более 255 символов.",
            },
        }

        class Media:
            css = {
                'all': ('css/interview_form.css',)  # Подключение CSS файла
            }
            js = ('js/interview_form.js',)  # Подключение JavaScript файла
