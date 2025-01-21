import json

from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect, get_object_or_404
from ..forms import InterviewForm
from ..models import Interview, InterviewTaskItem
from tasks.models import TaskItem, CodeQuestion, OpenQuestion, MultipleChoiceQuestion


def interview_list_view(request):
    interviews = Interview.objects.select_related('selection__resume__candidate__user').all()
    return render(request, 'interviews/interview_list.html', {'interviews': interviews})

def interview_create_view(request):
    if request.method == 'POST':
        form = InterviewForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('interview_list')  # Перенаправление на список интервью
    else:
        form = InterviewForm()
    return render(request, 'interviews/interview_form.html', {'form': form})

def interview_edit_view(request, pk):
    interview = get_object_or_404(Interview, pk=pk)
    if request.method == 'POST':
        form = InterviewForm(request.POST, request.FILES, instance=interview)
        if form.is_valid():
            form.save()
            return redirect('interview_list')
    else:
        form = InterviewForm(instance=interview)
    return render(request, 'interviews/interview_form.html', {'form': form})

def interview_delete_view(request, pk):
    interview = get_object_or_404(Interview, pk=pk)
    if request.method == 'POST':
        interview.delete()
        return redirect('interview_list')
    return render(request, 'interviews/interview_confirm_delete.html', {'interview': interview})



def interview_candidate_view(request):
    """
    Представление для отображения собеседования с учетом уже данных ответов.
    """
    interview_id = request.GET.get('interview_id')
    interview = get_object_or_404(Interview, id=interview_id)

    # Проверка возможности редактирования
    current_time = now()
    end_time = interview.start_time + timedelta(minutes=interview.duration)
    is_editable = request.user != interview.selection.interviewer and current_time <= end_time

    tasks_data = []
    for task in TaskItem.objects.filter(interviewtaskitem__interview=interview):
        task_data = {
            "id": task.id,
            "title": task.title,
            "description": task.task_condition,
            "interview_id": interview_id,
        }

        interview_task_item = InterviewTaskItem.objects.filter(interview=interview, task_item=task).first()

        if CodeQuestion.objects.filter(task_item=task).exists():
            code_task = CodeQuestion.objects.get(task_item=task)
            task_data.update({
                "type": "code",
                "input_data": code_task.input_data or "",
                "output_data": code_task.output_data or "",
                "is_code_run": code_task.is_code_run,
                "code": interview_task_item.candidate_answer if interview_task_item else "",
            })
        elif OpenQuestion.objects.filter(task_item=task).exists():
            task_data.update({
                "type": "open-question",
                "answer": interview_task_item.candidate_answer if interview_task_item else "",
            })
        elif MultipleChoiceQuestion.objects.filter(task_item=task).exists():
            choices = MultipleChoiceQuestion.objects.filter(task_item=task)
            task_data.update({
                "type": "multiple-choice",
                "options": [{"text": choice.answer_text, "is_correct": choice.is_correct_answer} for choice in choices],
                "selected_option": interview_task_item.candidate_answer if interview_task_item else "",
            })

        tasks_data.append(task_data)

    context = {
        "interview": interview,
        "duration": interview.duration,
        "tasks": json.dumps(tasks_data, cls=DjangoJSONEncoder),
        "is_editable": is_editable,  # Передача флага редактирования
    }
    return render(request, "candidate/interview_candidate.html", context)
