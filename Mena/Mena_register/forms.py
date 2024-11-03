from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    birthdate = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    
    class Meta:
        model = User
        fields = ["username", "email", "birthdate", "password1", "password2"]