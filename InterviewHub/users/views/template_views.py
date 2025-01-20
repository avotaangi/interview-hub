from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.timezone import now

from ..forms.auth_form import RegisterForm, LoginForm
from ..models import Candidate, Interviewer

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from ..forms.auth_form import RegisterForm, LoginForm
from ..models import Candidate, Interviewer
from interviews.models import Interview

from resumes.models import Resume
from tasks.models import TaskItem


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Отладка данных
            print("User type:", form.cleaned_data.get('user_type'))
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Создание кандидата или интервьюера в зависимости от выбора
            user_type = form.cleaned_data.get('user_type')
            if user_type == 'candidate':
                Candidate.objects.create(user=user)
            elif user_type == 'interviewer':
                Interviewer.objects.create(user=user)

            messages.success(request, "Регистрация успешна. Теперь вы можете войти.")
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})

@login_required
def home_candidate_view(request):
    return render(request, 'candidate/home_candidate.html')

@login_required
def home_interviewer_view(request):
    user = request.user
    current_date = now()  # Текущая дата и время с учётом временной зоны

    # Запланированные собеседования
    upcoming_interviews = Interview.objects.filter(
        selection__interviewer__user=user,
        start_time__gte=current_date,  # Только будущие собеседования
    ).order_by("start_time")

    # Завершенные собеседования
    completed_interviews = Interview.objects.filter(
        selection__interviewer__user=user,
        start_time__lt=current_date,  # Только прошлые собеседования
    ).order_by("-start_time")

    # Подсчет количества собеседований
    interview_counts = Interview.objects.filter(
        selection__interviewer__user=user
    ).aggregate(
        upcoming_count=Count('id', filter=Q(start_time__gte=current_date)),
        completed_count=Count('id', filter=Q(start_time__lt=current_date))
    )

    # Все резюме, отсортированные по ФИО кандидатов
    resumes = Resume.objects.select_related("candidate__user").order_by(
        "candidate__user__last_name", "candidate__user__first_name"
    )

    # Все задания, отсортированные по названию
    tasks = TaskItem.objects.all().order_by("title")

    context = {
        "upcoming_interviews": upcoming_interviews,
        "completed_interviews": completed_interviews,
        "resumes": resumes,
        "tasks": tasks,
        "upcoming_count": interview_counts['upcoming_count'],
        "completed_count": interview_counts['completed_count'],
    }
    return render(request, "interviewer/home_interviewer.html", context)

@login_required
def home_view(request):
    user = request.user
    try:
        candidate = Candidate.objects.get(user=user)
        return redirect('home_candidate')  # Перенаправляем на страницу кандидата
    except Candidate.DoesNotExist:
        pass  # Пользователь не кандидат

    try:
        # Проверяем, является ли пользователь интервьюером
        interviewer = Interviewer.objects.get(user=user)
        return redirect('home_interviewer')  # Перенаправляем на страницу интервьюера
    except Interviewer.DoesNotExist:
        pass  # Пользователь не интервьюер

    # Если роль не определена, перенаправляем на страницу по умолчанию
    return redirect('home')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Вы успешно вошли в систему.")
            return redirect('account')  # Перенаправляем на страницу аккаунта после успешного логина
        else:
            messages.error(request, "Неверные учетные данные.")
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def custom_logout_view(request):
    # Выход пользователя
    logout(request)
    messages.success(request, "Вы успешно вышли из системы.")
    return redirect('login')  # Или на любую другую страницу