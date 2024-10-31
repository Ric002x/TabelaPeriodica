from django import forms

from ..models import User
from ..validators import ResetPasswordValidator


class ResetPasswordForm(forms.ModelForm):
    new_password = forms.CharField(
        label="Nova Senha",
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••'
        }),
        error_messages={
            'required': 'Preencha com sua nova senha!',
        },
        help_text=('A senha precisa ter pelo menos 8 caracteres. '
                   'Tambem deve conter letras maiúsculas e números.'),
    )

    repeat_password = forms.CharField(
        label="Repita sua senha",
        required=True,
        error_messages={
            'required': 'Preencha com sua nova senha!',
        },
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••'
        }),
    )

    class Meta:
        model = User

        fields = ["new_password", "repeat_password"]

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        ResetPasswordValidator(data=self.cleaned_data)
        return super_clean
