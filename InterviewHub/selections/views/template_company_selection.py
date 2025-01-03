from ..forms.company_selection_form import CompanySelectionForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from ..models import CompanySelection


def company_selection_create(request):
    if request.method == 'POST':
        form = CompanySelectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')  # Перенаправление после успешного сохранения
        else:
            return render(request, 'selections/company_selection_form.html', {'form': form})
    else:
        form = CompanySelectionForm()
        return render(request, 'selections/company_selection_form.html', {'form': form})


def company_selection_view(request, pk=None):
    """
    Представление для создания или редактирования отбора компании.
    """
    if pk:
        # Если передан pk, получаем существующую запись
        instance = get_object_or_404(CompanySelection, pk=pk)
    else:
        # Иначе создаем новую запись
        instance = None

    if request.method == 'POST':
        # Если отправлен POST-запрос, заполняем форму данными
        form = CompanySelectionForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()  # Сохраняем данные формы
            return redirect('success/')  # Перенаправление после сохранения
    else:
        # Если GET-запрос, показываем пустую или заполненную форму
        form = CompanySelectionForm(instance=instance)

    # Рендеринг шаблона
    return render(request, 'selections/company_selection_detailed.html', {'form': form})


def company_selection_success(request):
    """
    Представление для отображения успешного результата после сохранения формы.
    """
    return HttpResponse("<h1>Форма успешно сохранена!</h1>")