from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .forms import *
from rolepermissions.decorators import has_permission_decorator

@login_required(login_url='login/')
def index(request):
    return render(request, 'principal/pagina_principal2.html', {'current_user': request.user})


@login_required(login_url='login/')
@has_permission_decorator('can_access_admin')
def modulo_admin(request):
    return render(request, 'modulos/modulo_administracion.html')


@login_required(login_url='login/')
@has_permission_decorator('can_access_reservas')
def modulo_reservas(request):
    return render(request, 'modulos/modulo_reservas.html')


@login_required(login_url='login/')
@has_permission_decorator('can_access_recepcion')
def modulo_recepcion(request):
    return render(request, 'modulos/modulo_recepcion.html')


@login_required(login_url='login/')
@has_permission_decorator('can_access_mantenimiento')
def modulo_mantenimiento(request):
    return render(request, 'modulos/modulo_mantenimiento.html')


@login_required(login_url='login/')
@has_permission_decorator('can_access_dashboard')
def modulo_dashboard(request):
    return render(request, 'modulos/modulo_dashboard.html')


@login_required(login_url='login/')
@has_permission_decorator('can_list_usuario')
def userlist(request):
    all_user = Usuario.objects.all().order_by('username')
    return render(request,'usuarios/list.html',{'all_user':all_user})


@login_required(login_url='login/')
@has_permission_decorator('can_list_tdr')
def tdrlist(request):
    all_tdr = TdRecurso.objects.all().order_by('description')
    return render(request, 'tdr/list.html', {'all_tdr': all_tdr})


@login_required(login_url='login/')
@has_permission_decorator('can_list_tdr')
def tdrdetail(request, id_tdr):
    tdr = get_object_or_404(TdRecurso, pk=id_tdr)
    return render(request, 'tdr/detail.html', {'tdr': tdr})


@login_required(login_url='login/')
@has_permission_decorator('can_delete_recurso')
def deleterecurso(request,id_tdr,id_r):
    tdr = get_object_or_404(TdRecurso, pk=id_tdr)
    recurso = get_object_or_404(Recurso,pk=id_r)
    #recurso.delete()
    return render(request,'tdr/delete.html',{
        'tdr' : tdr,
        'recurso': recurso
    })


@login_required(login_url='login/')
@has_permission_decorator('can_delete_recurso')
def deleterecursonconfirm(request,id_tdr,id_r):
    tdr = get_object_or_404(TdRecurso, pk=id_tdr)
    recurso = get_object_or_404(Recurso, pk=id_r)
    recurso.delete()
    return redirect('polireserva:tdrdetail', tdr.id_tdr)


@login_required(login_url='login/')
@has_permission_decorator('can_delete_tdr')
def deletetdr(request,id_tdr):
    tdr = get_object_or_404(TdRecurso, pk=id_tdr)
    return render(request,'tdr/deletetdr.html',{'tdr': tdr})


@login_required(login_url='login/')
@has_permission_decorator('can_delete_tdr')
def deletetdrconfirm(request,id_tdr):
    tdr = get_object_or_404(TdRecurso, pk=id_tdr)
    tdr.delete()
    return redirect('polireserva:tdrlist')


@login_required(login_url='login/')
@has_permission_decorator('can_add_tdr')
def tdrfill(request):
    tdrflag = False
    if request.method == 'POST':
        form = TdRecursoFillForm(request.POST)
        if form.is_valid():
            new_tdr = form.save(commit=False)
            new_tdr.save()
            tdrflag = True
            return redirect('../')
    else:
        form = TdRecursoFillForm()
    return render(request, 'tdr/tdrfill.html', {'form': form})


## METODOS DE RESERVA ##
@login_required(login_url='login/')
@has_permission_decorator('can_list_reserva')
def reservalist(request):
    all_reservas = Reservas.objects.all().order_by('date_i')
    return render(request, 'reservas/listareservas.html', {'all_reservas': all_reservas})


@login_required(login_url='login/')
@has_permission_decorator('can_list_reserva')
def reservadetail(request, id_R):
    reserva = get_object_or_404(Reservas, pk=id_R)
    return render(request, 'reservas/reservasdetail.html', {'reserva': reserva})


@login_required(login_url='login/')
@has_permission_decorator('can_add_reserva')
def newreserva(request):
    reservaflag = False
    if request.method == 'POST':
        form = ReservasForm(request.POST)
        if form.is_valid():
            new_reserva = form.save(commit=False)
            new_reserva.user = request.user
            new_reserva.save()
            form.save_m2m()
            reservaflag = True
            return redirect('../')
    else:
        form = ReservasForm()
    return render(request, 'reservas/newreserva.html', {'form': form})


@login_required(login_url='login/')
@has_permission_decorator('can_add_recurso')
def recursofill(request, id_tdr):
    tdr = get_object_or_404(TdRecurso, pk=id_tdr)
    recursoflag = False
    if request.method == 'POST':
        form = RecursoFillForm(request.POST)
        if form.is_valid():
            new_r = form.save(commit=False)
            new_r.id_tdr = tdr
            new_r.save()
            recursoflag = True
            return redirect('../')
    else:
        form = RecursoFillForm()
    return render(request, 'tdr/recursofill.html', {'form': form,
                                                    'tdr': tdr})


