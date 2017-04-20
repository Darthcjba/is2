
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required(login_url='login/')
def index(request):
    return render(request, 'principal/pagina_principal.html', {'current_user': request.user})

def register(request):
    return render(request, 'registration/register.html', {'current_user': request.user})