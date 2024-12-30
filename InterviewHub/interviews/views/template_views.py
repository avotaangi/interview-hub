from django.shortcuts import render, redirect, get_object_or_404

from ..models import Interview
from ..forms import InterviewForm


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

