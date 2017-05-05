# log/forms.py
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from log import models


# If I dont do this I cannot use Bootstrap CSS
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Nombre de usuario", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Contrasena", max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))


class SignUpForm(UserCreationForm):
    username = forms.CharField(label="Nombre de usuario", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    first_name = forms.CharField(label="Nombre", max_length=30, required=False, help_text='Opcional.',
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'nombre'}))
    last_name = forms.CharField(label="Apellido", max_length=30, required=False, help_text='Opcional.',
                                widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'apellido'}))
    email = forms.EmailField(max_length=254,
                             widget=forms.EmailInput(attrs={'class': 'form-control validate', 'name': 'email'}),
                             help_text='Requiredo. Ingresa un email valido.')
    password1 = forms.CharField(label="Contrasena", max_length=30,
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))
    password2 = forms.CharField(label="Repetir contrasena", max_length=30,
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'repeat_password'}))


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class UsuarioForm(forms.ModelForm):

    cin = forms.CharField(label="C.I.", max_length=10,
                          widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'cin'}))
    ladder = forms.ChoiceField(choices=models.LADDER_CHOICES, widget=forms.Select(attrs={'class': 'form-control', 'name': 'ladder'}))

    phone = forms.CharField(label="Telefono", max_length=10,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'telefono'}))

    class Meta:
        model = models.Usuario
        fields = ['cin', 'ladder', 'phone']

    def save(self, commit=True):
        user = super(UsuarioForm, self).save(commit=False)
        user.cin = self.cleaned_data["cin"]
        user.ladder = self.cleaned_data["ladder"]
        user.phone = self.cleaned_data["phone"]

        if commit:
            user.save()
        return user

