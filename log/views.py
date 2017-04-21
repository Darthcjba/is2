# Create your views here.
# log/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from log import forms
from django.contrib.auth import login, authenticate


# Create your views here.
# this login required decorator is to not allow to any
# view without authenticating
@login_required(login_url="login/")
def home(request):
    return render(request, "principal/pagina_principal.html")


def register(request):
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        extra_form = forms.UsuarioForm(request.POST or None)
        if form.is_valid() and extra_form.is_valid():
            new_user = form.save()
            new_extended_obj = extra_form.save(commit=False)
            # assign the user to the extended obj
            new_extended_obj.user = new_user
            new_extended_obj.username_id = new_user.id
            # write to database
            new_extended_obj.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = forms.SignUpForm()
        extra_form = forms.UsuarioForm()
    return render(request, 'registration/register.html', {'form': form, 'extra_form': extra_form})

