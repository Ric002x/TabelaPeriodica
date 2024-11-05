import re
from collections import defaultdict

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UsersValidatorsForCreate:
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
        self.validate_passwords_match()
        self.clean_email()
        self.clean_first_name()
        self.clean_last_name()
        self.clean_agree_to_terms()
        self.clean_username()

        if self.errors:
            raise self.ErrorClass(self.errors)  # type: ignore

    def validate_passwords_match(self, *args, **kwargs):
        password1 = self.data.get('password')
        password2 = self.data.get('password2')

        if password1 and password2 and password1 != password2:
            password_error = self.ErrorClass(
                'As senhas precisam ser iguais',
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
        password2 = self.data.get('password2')

        no_password_error = self.ErrorClass(
            "Esse campo é obrigatório",
            code="required"
        )
        if not password:
            self.errors['password'].append(no_password_error)
        else:
            self.strong_password(password)
        if not password2:
            self.errors['password2'].append(no_password_error)

        return password

    def clean_first_name(self, *args, **kwargs):
        first_name = self.data.get('first_name')
        if not first_name:
            self.errors['first_name'].append(self.ErrorClass(
                'Esse campo é obrigatório',
                code='required'
            ))

    def clean_last_name(self, *args, **kwargs):
        last_name = self.data.get('last_name')
        if not last_name:
            self.errors['last_name'].append(self.ErrorClass(
                'Esse campo é obrigatório',
                code='required'
            ))

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

    def clean_username(self, *args, **kwargs):
        username = self.data.get('username')
        if not username:
            self.errors['username'].append(self.ErrorClass(
                'Esse campo é obrigatório',
                code='blank'
            ))

        if username:
            if not re.match(r'^[\w-]+$', username):
                self.errors['username'].append(
                    self.ErrorClass(
                        'O nome de usuário só pode conter letras, '
                        'números, hifens (-) e sublinhados (_).',
                        code='invalid'
                    )
                )
            if len(username) < 5:
                self.errors['username'].append(
                    self.ErrorClass(
                        'O nome de usuário precisa '
                        'ter o mínimo de 5 caracteres',
                        code='min_length'
                    )
                )
            if len(username) > 20:
                self.errors['username'].append(
                    self.ErrorClass(
                        'O nome não pode ultrapassar '
                        'o máximo de 20 caracteres',
                        code='max_length'
                    )
                )
        return username


class UsersValidatorsForUpdate(UsersValidatorsForCreate):
    def __init__(self, data, errors=None, ErrorClass=None):
        super().__init__(data, errors, ErrorClass)

    def final_clean(self, *args, **kwargs):
        if 'username' in self.data:
            self.clean_username()
        if 'email' in self.data:
            self.clean_email()
        if 'first_name' in self.data:
            self.clean_first_name()
        if 'last_name' in self.data:
            self.clean_last_name()
        if 'password' in self.data or 'password2' in self.data:
            self.errors['password'].append(
                self.ErrorClass(
                    'Não é possível atualizar a senha neste endpoint',
                    code='forbidden_field'
                )
            )

        if self.errors:
            raise self.ErrorClass(self.errors)  # type: ignore


class ResetPasswordValidator:
    def __init__(self, data, errors=None, ErrorClass=None):
        self.data = data
        self.errors = defaultdict(list) if errors is None else errors
        self.ErrorClass = ValidationError if ErrorClass is None else ErrorClass
        self.final_clean()

    def final_clean(self, *args, **kwargs):
        self.clean_password()
        self.validate_passwords_match()

        if self.errors:
            raise self.ErrorClass(self.errors)  # type: ignore

    def validate_passwords_match(self, *args, **kwargs):
        password1 = self.data.get('new_password')
        password2 = self.data.get('repeat_password')

        if password1 and password2 and password1 != password2:
            password_error = self.ErrorClass(
                'As senhas precisam ser iguais',
                code="invalid"
            )
            self.errors['new_password'].append(password_error)
            self.errors['repeat_password'].append(password_error)

    def strong_password(self, password):
        regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[1-9]).{8,}$')

        if not regex.match(password):
            self.errors['new_password'].append(self.ErrorClass(
                'A senha deve contar pelo menos 8 caracteres, '
                'incluindo letras maiúsculas e números',
                code='invalid',
            ))

    def clean_password(self, *args, **kwargs):
        password = self.data.get('new_password')
        password2 = self.data.get('repeat_password')

        no_password_error = self.ErrorClass(
            "Esse campo é obrigatório",
            code="required"
        )
        if not password:
            self.errors['new_password'].append(no_password_error)
        else:
            self.strong_password(password)
        if not password2:
            self.errors['repeat_password'].append(no_password_error)

        return password
