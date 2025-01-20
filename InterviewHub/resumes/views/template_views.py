from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def resume_interviewer_view(request):
    """
    Представление для отображения страницы с резюме интервьюера.
    """
    # Если вам нужно передать контекст, добавьте его сюда
    context = {}
    return render(request, "interviewer/resume_interviewer.html", context)

@login_required
def resume_candidate_view(request):
    """
    Представление для отображения страницы с резюме интервьюера.
    """
    # Если вам нужно передать контекст, добавьте его сюда
    context = {}
    return render(request, "candidate/resume_candidate.html", context)