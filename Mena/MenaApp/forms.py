from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Period
from .models import Symptoms, Post, Calendar

class RegisterForm(UserCreationForm):
    username = forms.EmailField(required=True,widget=forms.EmailInput(attrs={
        'class': 'input-field',
        'placeholder': 'Username'
    }))
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

class PeriodForm(forms.ModelForm):
    class Meta:
        model = Period
        fields = ['start_date', 'end_date', 'day']

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'Username'
            }),
        }

class PostsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'Title'
            }),

            'content': forms.Textarea(attrs={ 
                'class': 'text-field', 
                'placeholder': 'Type Here...' 
            }),
        }

class SymptomsForm(forms.ModelForm):
    class Meta:
        model = Symptoms
        fields = ['phase']

class CalendarPinForm(forms.Form):
    day = forms.IntegerField(min_value=1, max_value=31, label="Day")
    is_pinned = forms.BooleanField(required=False, label="Pin this day")

class PinForm(forms.Form):
    day = forms.IntegerField(
        min_value=1,
        max_value=31,
        label="Day to Pin/Unpin",
        widget=forms.NumberInput(attrs={'placeholder': 'Enter a day'}),
    )