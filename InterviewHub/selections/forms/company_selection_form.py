from django import forms
from ..models import CompanySelection

class CompanySelectionForm(forms.ModelForm):
    class Meta:
        model = CompanySelection
        fields = ['interviewer', 'resume', 'status']
        widgets = {
            'interviewer': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Выберите интервьюера'}),
            'resume': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Выберите резюме'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'interviewer': 'Интервьюер',
            'resume': 'Резюме',
            'status': 'Статус',
        }

    def clean_status(self):
        status = self.cleaned_data.get('status')
        if status not in dict(CompanySelection.selection_status_choices):
            raise forms.ValidationError('Некорректный статус.')
        return status
