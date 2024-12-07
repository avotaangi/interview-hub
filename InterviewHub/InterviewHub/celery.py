from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Устанавливаем настройки Django по умолчанию для Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'InterviewHub.settings')

app = Celery('InterviewHub')

# Загружаем настройки из Django settings с префиксом CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически обнаруживаем задачи из приложений
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

app.conf.beat_schedule = {
    'send_reminders_every_hour': {
        'task': 'interviews.tasks.send_interview_reminder',
        'schedule': crontab(minute='*'),  # Каждую минуту
    },
}

app.conf.beat_schedule = {
    # Архивация "Отклоненных" CompanySelection раз в неделю
    'archive_rejected_selections': {
        'task': 'selections.tasks.archive_rejected_company_selections',
        'schedule': crontab(day_of_week='sunday', hour=0, minute=0),  # Каждый воскресенье в 00:00
    },
}
