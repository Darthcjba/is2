#log/forms.py
from django.contrib.auth.forms import AuthenticationForm
from django import forms

#If I dont do this I cannot use Bootstrap CSS
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Nombre de usuario", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Contrasena", max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))