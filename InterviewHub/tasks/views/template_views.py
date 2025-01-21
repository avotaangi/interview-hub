from django.shortcuts import render, get_object_or_404
from ..models import TaskItem

def tasks_with_choices(request):
    query = request.GET.get('query', '').strip()
    tasks = TaskItem.objects.filter(multiplechoicequestion__isnull=False)

    if query:
        tasks = tasks.filter(title__icontains=query)

    return render(request, 'tasks/tasks_list.html', {
        'title': 'Задания с вариантами ответов',
        'tasks': set(tasks),
    })

def tasks_with_open_questions(request):
    query = request.GET.get('query', '').strip()
    tasks = TaskItem.objects.filter(openquestion__isnull=False)

    if query:
        tasks = tasks.filter(title__icontains=query)

    return render(request, 'tasks/tasks_list.html', {
        'title': 'Задания с открытыми вопросами',
        'tasks': set(tasks),
    })

def tasks_with_code_questions(request):
    query = request.GET.get('query', '').strip()
    tasks = TaskItem.objects.filter(codequestion__isnull=False)

    if query:
        tasks = tasks.filter(title__icontains=query)

    return render(request, 'tasks/tasks_list.html', {
        'title': 'Задания с написанием кода',
        'tasks': set(tasks),
    })

def all_tasks(request):
    query = request.GET.get('query', '').strip()
    tasks = TaskItem.objects.all()

    if query:
        tasks = tasks.filter(title__icontains=query)

    return render(request, 'tasks/tasks_list.html', {
        'title': 'Все задания',
        'tasks': set(tasks),
    })
def task_detail(request, task_id):
    task = get_object_or_404(TaskItem, id=task_id)
    return render(request, 'tasks/task_detail.html', {'task': task})