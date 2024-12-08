from celery import shared_task
from django.utils.timezone import now, timedelta
from .models import CompanySelection


@shared_task
def archive_rejected_company_selections():
    # Определяем дату 6 месяцев назад
    six_months_ago = now() - timedelta(days=6 * 30)  # 6 месяцев, приближенно 30 дней в месяце

    # Фильтруем записи, которые нужно архивировать
    rejected_selections = CompanySelection.objects.filter(
        status="Отклонен",
        created_at__lt=six_months_ago
    )

    # Архивируем записи (удаляем или помечаем как архивные)
    count = rejected_selections.count()
    rejected_selections.delete()

    return f"Archived {count} rejected CompanySelections older than 6 months."
