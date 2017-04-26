from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from models import TdRecurso
from .forms import TdRecursoFillForm,RecursoFillForm


@login_required(login_url='login/')
def index(request):
    return render(request, 'principal/pagina_principal.html', {'current_user': request.user})

def tdrlist(request):
    all_tdr = TdRecurso.objects.all()
    return render(request, 'tdr/list.html', {'all_tdr':all_tdr})


def tdrdetail(request, id_tdr):
    tdr = get_object_or_404(TdRecurso, pk=id_tdr)
    return render(request,'tdr/detail.html', {'tdr':tdr})


def tdrfill(request):
    tdrflag = False
    if request.method == 'POST':
        form = TdRecursoFillForm(request.POST)
        if form.is_valid():

            new_tdr=form.save(commit=False)
            new_tdr.save()
            tdrflag = True
            return redirect('../')
    else:
        form = TdRecursoFillForm()
    return render(request,'tdr/tdrfill.html',{'form':form})


def recursofill(request,id_tdr):
    tdr = get_object_or_404(TdRecurso, pk=id_tdr)
    recursoflag = False
    if request.method == 'POST':
        form = RecursoFillForm(request.POST)
        if form.is_valid():

            new_r=form.save(commit=False)
            new_r.id_tdr= tdr
            new_r.save()
            recursoflag = True
            return redirect('../')
    else:
        form = RecursoFillForm()
    return render(request,'tdr/recursofill.html',{'form':form,
                                                  'tdr':tdr})