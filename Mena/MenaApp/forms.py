from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={
        'class': 'input-field',
        'placeholder': 'Email Address'
    }))
    birthdate = forms.DateField(required=True, widget=forms.DateInput(attrs={
        'class': 'input-field',
        'placeholder': 'dd/mm/yyyy',
        'type':'date'
    }))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input-field',
            'placeholder': 'Password'
    }))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input-field',
            'placeholder': 'Confirm Password'
    }))
    
    class Meta:
        model = User
        fields = ["username", "email", "birthdate", "password1", "password2"]
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'Username'
            }),
        }