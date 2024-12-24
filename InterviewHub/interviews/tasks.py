from celery import shared_task
from django.core.mail import send_mail
from django.utils.timezone import now, timedelta
from .models import Interview

@shared_task
def send_interview_reminder():
    # Получаем текущее время
    current_time = now()
    # Фильтруем собеседования, которые начинаются в пределах следующего часа
    upcoming_interviews = Interview.objects.filter(
        start_time__gte=current_time + timedelta(hours=1),  # Собеседования, которые начинаются через час или позже
        start_time__lt=current_time + timedelta(hours=1, minutes=1)  # И которые начинаются в пределах следующего часа и одной минуты
    )
    for interview in upcoming_interviews:
        send_mail(
            subject='Напоминание о собеседовании',
            message=(
                f'Здравствуйте, {interview.selection.resume.candidate.user.first_name}! '
                f'Напоминаем, что ваше собеседование в компанию '
                f'"{interview.selection.interviewer.company.name}" начнется через 1 час.'
            ),
            from_email='admin@inteviewhub.ru',
            recipient_list=[interview.selection.resume.candidate.user.email],
        )
