from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from models import TdRecurso

@login_required(login_url='login/')
def index(request):
    return render(request, 'principal/pagina_principal.html', {'current_user': request.user})

def tdrlist(request):
    all_tdr = TdRecurso.objects.all()
    return render(request, 'tdr/list.html', {'all_tdr':all_tdr})


def tdrdetail(request, id_tdr):
    tdr = get_object_or_404(TdRecurso, pk=id_tdr)
    return render(request,'tdr/detail.html', {'tdr':tdr})