import re
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[1-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError(
            'A senha deve contar pelo menos 8 caracteres, '
            'incluindo letras maiúsculas e números',
            code='invalid',
        )


class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        label='Nome de usuário',
        widget=forms.TextInput(attrs={
            'placeholder': 'Insira aqui seu nome de usuário. '
            'Ex.: LucasOliveira22'
        }),
        min_length=5,
        max_length=20,
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
        validators=[strong_password],
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

        error_messages = {
            'first_name': {
                'required': 'Esse campo é obrigatório',
            },

            'last_name': {
                'required': 'Esse campo é obrigatório',
            },

            'email': {
                'required': 'Esse campo é obrigatório',
                'invalid': 'Insira um endereço de e-mail válido',
            },

            'username': {
                'required': 'Esse campo é obrigatório',
                'unique': 'Inválido. Nome de usuário já existente',
            },
        }

        validators = {
            'password': [strong_password],
        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Insira aqui seu primeiro nome. Ex.: Lucas'
            }),

            'last_name': forms.TextInput(attrs={
                'placeholder': 'Insira aqui seu sobrenome. Ex.: Oliveira',
            }),

            'username': forms.TextInput(attrs={
                'placeholder': 'Insira aqui seu nome de usuário. '
                'Ex.: LucasOliveira22',
            }),
            'email': forms.TextInput(attrs={
                'placeholder': 'Insira aqui seu e-mail. '
                'Ex.: olilucas@email.com',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():

            # Todos os campos são required, logo:
            field.required = True
            field.error_messages = {'required': 'Esse campo é obrigatório'}

            # Se o campo tiver required = True, coloque: "{'required': 'Esse campo é obrigatório'}"     # noqa: E501
            """if field.required:
                field.error_messages = {'required': 'Esse campo é obrigatório'}"""     # noqa: E501

            if field_name == 'username':
                field.error_messages.update(
                    {'unique': 'Inválido. Nome de usuário já existente'})
                field.error_messages.update(
                    {'min_length': 'Este campo precisa ter '
                     'o mínimo de 5 caractéres'})
                field.error_messages.update(
                    {'max_length': 'Este campo precisa ter '
                     'o máximo de 20 caractéres'})

            if field_name == 'email':
                field.error_messages.update({
                    'required': 'Esse campo é obrigatório'})

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

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            passoword_error = ValidationError(
                'As senhas precisam ser iguais',
                code='invalid'
            )
            raise ValidationError({
                'password': passoword_error,
                'password2': [passoword_error],
            })
