from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput
    )
    region = forms.CharField(
        label='地址',
        max_length=50,
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password')