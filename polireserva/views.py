
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def index(request):
    """A view that can only be accessed by logged-in users"""
    return render(request, 'principal/pagina_principal.html', {'current_user': request.user})