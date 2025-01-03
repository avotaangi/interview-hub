from django import template
from datetime import datetime
from ..models import Interview

register = template.Library()

# 1. Создание простого шаблонного тега
@register.simple_tag
def current_date(format_string="%Y-%m-%d"):
    """Возвращает текущую дату в указанном формате"""
    return datetime.now().strftime(format_string)

# 2. Создание шаблонного тега с контекстными переменными
@register.simple_tag(takes_context=True)
def get_interviews_by_status(context, status):
    """Возвращает список интервью с указанным статусом из контекста"""
    interviews = context.get('interviews', Interview.objects.all())
    return interviews.filter(status=status)

# 3. Создание шаблонного тега, возвращающего набор запросов
@register.simple_tag
def get_upcoming_interviews(limit=5):
    """Возвращает список предстоящих интервью"""
    return Interview.objects.filter(start_time__gte=datetime.now()).order_by('start_time')[:limit]
