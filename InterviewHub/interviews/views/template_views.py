from django.shortcuts import render

from ..models import Interview


def interview_list_view(request):
    interviews = Interview.objects.select_related('selection__resume__candidate__user').all()
    return render(request, 'interviews/interview_list.html', {'interviews': interviews})