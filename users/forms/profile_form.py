from django import forms
from django.contrib.auth.models import User
from ..models import Profile


class UpdateUserForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=20,
        min_length=3,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
        )
    last_name = forms.CharField(
        max_length=20,
        min_length=3,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
        )
    username = forms.CharField(
        max_length=20,
        min_length=3,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
        )
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].initial = None


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))

    class Meta:
        model = Profile
        fields = ['avatar']

        labels = {
            'avatar': 'Foto de perfil'
        }
