from django import template
from datetime import datetime

from InterviewHub.testlab.models import MyModel

register = template.Library()

@register.simple_tag
def current_date(format_string="%Y-%m-%d"):
    """Возвращает текущую дату в указанном формате"""
    return datetime.now().strftime(format_string)


@register.simple_tag(takes_context=True)
def calculate_sum(context, key):
    """Вычисляет сумму значений списка из контекста по ключу"""
    values = context.get(key, [])
    if not isinstance(values, list):
        return "Invalid data"
    return sum(values)

@register.simple_tag
def get_filtered_objects(filter_field, filter_value, limit=10):
    """Возвращает отфильтрованные объекты модели MyModel"""
    return MyModel.objects.filter(**{filter_field: filter_value}).order_by('-created_at')[:limit]

