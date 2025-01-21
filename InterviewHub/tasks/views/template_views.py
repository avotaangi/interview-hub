from django.shortcuts import render, get_object_or_404
from ..models import TaskItem

def tasks_with_choices(request):
    tasks = set(TaskItem.objects.filter(multiplechoicequestion__isnull=False))
    return render(request, 'tasks/tasks_list.html', {'tasks': tasks, 'title': 'Задания с вариантами ответов'})

def tasks_with_open_questions(request):
    tasks = set(TaskItem.objects.filter(openquestion__isnull=False))
    return render(request, 'tasks/tasks_list.html', {'tasks': tasks, 'title': 'Задания с открытыми вопросами'})

def tasks_with_code_questions(request):
    tasks = set(TaskItem.objects.filter(codequestion__isnull=False))
    return render(request, 'tasks/tasks_list.html', {'tasks': tasks, 'title': 'Задания с написанием кода'})

def task_detail(request, task_id):
    task = get_object_or_404(TaskItem, id=task_id)
    return render(request, 'tasks/task_detail.html', {'task': task})
