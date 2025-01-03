from django.shortcuts import render, redirect
from ..forms.company_selection_form import CompanySelectionForm

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
