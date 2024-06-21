import re
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=[A-Z])(?=.*[1-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError(
            'A senha deve contar pelo menos 8 caracteres, '
            'incluindo letras maiúsculas e números',
            code='invalid',
        )


class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        min_length=5, max_length=20,
        label='Nome de usuário',
        help_text='O nome de usuário deverá contar menos de 20 '
        'caracteres. Use somente letras, números e _/#/@/%/$',
        widget=forms.TextInput(attrs={
            'placeholder': 'Insira aqui seu nome de usuário. '
            'Ex.: LucasOliveira22',
        }),
        error_messages={
            'required': 'Esse campo é obrigatório',
        },
        required=True,
    )

    password = forms.CharField(
        label='Senha',
        help_text=('A senha precisa ter pelo menos 8 caracteres. '
                   'Tambem deve conter letras maiúsculas e números.'),
        widget=forms.PasswordInput(),
        required=True,
        validators=[strong_password],
        error_messages={
            'required': 'Esse campo é obrigatório',
        },
    )

    password2 = forms.CharField(
        label='Confirme sua senha',
        widget=forms.PasswordInput(),
        required=True,
        error_messages={
            'required': 'Esse campo é obrigatório'
        },
    )

    email = forms.EmailField(
        required=True, label='E-mail',
        error_messages={
            'required': 'Esse campo é obrigatório'
        },
        widget=forms.TextInput(attrs={
                'placeholder': 'Insira aqui seu e-mail. '
                'Ex.: olilucas@email.com',
            }),
        )

    first_name = forms.CharField(
        min_length=3, max_length=50,
        label='Nome',
        widget=forms.TextInput(attrs={
            'placeholder': 'Insira aqui seu nome. '
            'Ex.: Ana',
        }),
        error_messages={
            'required': 'Esse campo é obrigatório',
        },
        required=True,
    )

    last_name = forms.CharField(
        min_length=3, max_length=50,
        label='Sobrenome',
        widget=forms.TextInput(attrs={
            'placeholder': 'Insira aqui seu sobrenome. '
            'Ex.: Oliveira',
        }),
        error_messages={
            'required': 'Esse campo é obrigatório',
        },
        required=True,
    )

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username',
            'email', 'password', 'password2',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Verifica se já existe tal email cadastro
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                "invalido. Já existe um usuário cadastrado com esse email",
                code='unique'
            )
        return email
    
    # Verifica as senhas
    def clean(self):
        cleaned_data = super().clean()

        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password != password2:
            passoword_error = ValidationError(
                'As senhas precisam ser iguais',
                code='invalid'
            )
            raise ValidationError({
                'password': passoword_error,
                'password2': [passoword_error],
                })
        return cleaned_data
