from django import forms
from ..models import Activity, ActivityLevel, ActivitySubject


class ActivityForm(forms.ModelForm):
    title = forms.CharField(
        required=True,
        label='Título',
        error_messages={
            'required': 'Campo obrigatório'
        },
        widget=forms.TextInput(attrs={
            'placeholder': 'O Ciclo da Água',
            'class': 'form-activity-input'
        }),
    )

    description = forms.CharField(
        required=True,
        label='Descrição',
        error_messages={
            'required': 'Campo obrigatório'
        },
        widget=forms.Textarea(attrs={
            'placeholder': 'Está atividade fala sobre o ciclo da água...',
            'class': 'form-activity-input'
        })
    )

    subject = forms.ModelChoiceField(
        label='Matéria',
        queryset=ActivitySubject.objects.all().order_by('name'),
        required=True,
        error_messages={
            'required': 'Campo obrigatório'
        },
        widget=forms.Select(attrs={
            'class': 'form-activity-input'
        })
    )

    level = forms.ModelChoiceField(
        label='Turma',
        queryset=ActivityLevel.objects.all(),
        required=True,
        error_messages={
            'required': 'Campo obrigatório'
        },
        widget=forms.Select(attrs={
            'class': 'form-activity-input',
            'onclick': 'teste()'
        })
    )

    file = forms.FileField(
        required=True,
        error_messages={
            'required': 'Campo obrigatório'
        },
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-activity-input',
            'accept': '.doc, .docx, .pdf'
        })
    )

    class Meta:
        model = Activity

        fields = ['title', 'description',
                  'level', 'subject', 'file']
