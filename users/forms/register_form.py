from django import forms
from django.contrib.auth.models import User

from ..validators import UsersValidatorsForCreate


class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        label='Nome de usuário',
        widget=forms.TextInput(attrs={
            'placeholder': 'Insira aqui seu nome de usuário. '
            'Ex.: LucasOliveira22'
        }),
        required=True,
        error_messages={
            'required': 'Esse campo é obrigatório',
        }
    )

    password = forms.CharField(
        label='Senha',
        help_text=('A senha precisa ter pelo menos 8 caracteres. '
                   'Tambem deve conter letras maiúsculas e números.'),
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••'
        }),
        required=True,
        error_messages={
            'required': 'Esse campo é obrigatório',
        },
    )

    password2 = forms.CharField(
        label='Confirme sua senha',
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••'
        }),
        required=True,
        error_messages={
            'required': 'Esse campo é obrigatório'
        },
    )

    agree_to_terms = forms.BooleanField(
        required=True,
        label="",
    )

    class Meta:
        model = User

        fields = [
            'first_name', 'last_name', 'username',
            'email', 'password', 'password2', 'agree_to_terms'
        ]

        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Insira aqui seu primeiro nome. Ex.: Lucas'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Insira aqui seu sobrenome. Ex.: Oliveira',
            }),
            'email': forms.TextInput(attrs={
                'placeholder': 'Insira aqui seu e-mail. '
                'Ex.: olilucas@email.com',
            }),
        }

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        UsersValidatorsForCreate(data=self.cleaned_data)
        return super_clean
