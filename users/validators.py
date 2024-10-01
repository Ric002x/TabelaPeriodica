import re
from collections import defaultdict

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UsersValidators:
    def __init__(self, data, errors=None, ErrorClass=None):
        self.data = data
        self.errors = defaultdict(list) if errors is None else errors
        self.ErrorClass = ValidationError if ErrorClass is None else ErrorClass
        self.final_clean()

    def strong_password(self, password):
        regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[1-9]).{8,}$')

        if not regex.match(password):
            self.errors['password'].append(self.ErrorClass(
                'A senha deve contar pelo menos 8 caracteres, '
                'incluindo letras maiúsculas e números',
                code='invalid',
            ))

    def final_clean(self, *args, **kwargs):
        self.clean_password()
        self.clean_email()
        self.clean_first_and_last_name()
        self.validate_passwords_match()
        self.clean_agree_to_terms()

        if self.errors:
            raise self.ErrorClass(self.errors)  # type: ignore

    def validate_passwords_match(self, *args, **kwargs):
        clean_data = self.data
        password1 = clean_data.get('password')
        password2 = clean_data.get('password2')

        if password1 != password2:
            password_error = self.ErrorClass(
                'As senha precisam ser iguais',
                code="invalid"
            )
            self.errors['password'].append(password_error)
            self.errors['password2'].append(password_error)

    def clean_email(self, *args, **kwargs):
        email = self.data.get('email')
        if not email:
            self.errors['email'].append(
                self.ErrorClass(
                    'Esse campo é obrigatório',
                    code='required'
                )
            )
        if User.objects.filter(email=email).exists():
            self.errors['email'].append(
                self.ErrorClass(
                    'Inválido! Já existe um usuário '
                    'cadastrado com esse email.',
                    code='unique'
                )
            )
        return email

    def clean_password(self, *args, **kwargs):
        password = self.data.get('password')
        if not password:
            self.errors['password'].append(self.ErrorClass(
                "Esse campo é obrigatório",
                code="required"
            ))
        self.strong_password(password)
        return password

    def clean_first_and_last_name(self, *args, **kwargs):
        first_name = self.data.get('first_name')
        last_name = self.data.get('last_name')

        cannot_be_empty_error = self.ErrorClass(
            'Esse campo é obrigatório',
            code='required'
        )
        if not first_name:
            self.errors['first_name'].append(cannot_be_empty_error)
        if not last_name:
            self.errors['last_name'].append(cannot_be_empty_error)

    def clean_agree_to_terms(self, *args, **kwargs):
        agreed = self.data.get('agree_to_terms')
        if agreed is False:
            self.errors['agree_to_terms'].append(
                self.ErrorClass(
                    'É necessário concordar com os'
                    ' termos para realizar o cadastro',
                    code='invalid'
                )
            )
        return agreed
