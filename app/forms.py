from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    # password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email', 'account_type')


class CustomUserChangeForm(UserChangeForm):
    # password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'account_type')


