from django.shortcuts import render

from .models import MyModel


def example_view(request):
    """Пример представления для отображения шаблона"""
    return render(request, 'testlab/example_template.html')

def example_context_variable(request):
    context = {
        'my_values': [10, 20, 30, 40]
    }
    return render(request, 'testlab/context_variable.html', context)

def example_queryset(request):
    """
    Представление для отображения страницы с использованием QuerySet из шаблонного тега.
    """
    context = {
        'static_queryset': MyModel.objects.filter(status='active').order_by('-created_at')[:10],
    }
    return render(request, 'testlab/queryset_example.html', context)