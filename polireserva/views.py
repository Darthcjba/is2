from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from models import TdRecurso

@login_required(login_url='login/')
def index(request):
    return render(request, 'principal/pagina_principal.html', {'current_user': request.user})

def tdrlist(request):
    all_tdr = TdRecurso.objects.all()
    context = {
        'all_tdr':all_tdr,
    }
    return render(request, 'tdr/list.html', context)


def tdrdetail(request, id_tdr):
    return HttpResponse("<h2>Detalles de Tipo de Recurso id: " + str(id_tdr) + "</h2>")