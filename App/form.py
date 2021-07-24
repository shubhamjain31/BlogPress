from django import forms
from froala_editor.widgets import FroalaEditor
from .models import *

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogModel
        fields = ['content']


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Username",                
                "class"       : "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder" : "Email",                
                "class"       : "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Enter Password",                
                "class"       : "form-control",
                "autocomplete":"on"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Re Enter Password",                
                "class"       : "form-control",
                "autocomplete":"on"
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
