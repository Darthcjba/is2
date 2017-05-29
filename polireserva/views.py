from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from rolepermissions.decorators import has_permission_decorator
from rolepermissions.roles import get_user_roles, assign_role
from .forms import *
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import date,datetime


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
@has_permission_decorator('can_list_usuarios')
def userlist(request):
    all_user = Usuario.objects.all().order_by('username')
    return render(request,'usuarios/list.html',{'all_user':all_user})


def rolelist(request,username_id):
    user= User.objects.get(id=username_id)
    roles = get_user_roles(user)
    return render(request,'usuarios/roles.html',{'user':user,
                                                 'roles':roles})

def roleassing(request,username_id):
    user=User.objects.get(id=username_id)
    return render(request, 'usuarios/addrole.html',{'user':user})


def roleassignation(request,username_id,role_id):
    user = User.objects.get(id=username_id)
    if role_id == 1:
        assign_role(user,'administrador')
    elif role_id == 2:
        assign_role(user,'usuario')
    elif role_id == 3:
        assign_role(user,'recepcionista')
    elif role_id == 4:
        assign_role(user,'tecnico')
    elif role_id == 5:
        assign_role(user,'invitado')
    else:
        redirect('polireserva:polindex')
    return redirect('polireserva:roleslist',username_id)

def mantenimientolist(request):
    all_man = Mantenimiento.objects.filter(estado="Encurso")
    all_need = Mantenimiento.objects.filter(estado="Enespera")
    return render(request,'mantenimiento/list.html',{'all_man': all_man,
                                                     'all_need':all_need})


def mantenimientonew(request):
    if request.method == 'POST':
        form = MantenimientoNewForm(request.POST)
        if form.is_valid():
            new_man = form.save(commit=False)
            new_man.user=request.user
            new_man.estado="Encurso"
            recurso=new_man.recurso
            recurso.status='Mantenimiento'
            recurso.save()
            new_man.save()
        return redirect('../')
    else:
        form = MantenimientoNewForm()
    return render(request, 'mantenimiento/new.html', {'form': form})

def mantenimientofin(request,id_M):
    man = get_object_or_404(Mantenimiento,pk=id_M)

    if request.method == 'POST':
        form = MantenimientoFinForm(request.POST)
        if form.is_valid():
            new_man=form.save(commit=False)
            man.report=new_man.report
            man.estado="Finalizado"
            recurso=man.recurso
            recurso.status='Disponible'
            recurso.save()
            man.save()
            return redirect('../../')
    else:
        form= MantenimientoFinForm()
    return render(request,'mantenimiento/fin.html',{'form':form,
                                                     'man':man})


def amantenimiento(request,id_M):
    man = get_object_or_404(Mantenimiento,pk=id_M)
    rec = man.recurso
    return render(request, 'mantenimiento/detail.html', {'man': man,
                                                       'rec': rec})

def enviarman(request,id_M):
    man = get_object_or_404(Mantenimiento,pk=id_M)
    man.estado="Encurso"
    rec=man.recurso
    rec.status="Mantenimiento"
    rec.save()
    man.save()
    return redirect('polireserva:mantenimientolist')

def recepcionlist(request):
    d=date.today()
    res_today=[]
    all_res=Reservas.objects.all()
    for res in all_res:
        if res.date_i.date == d :
            res_today.append(res)
    return render(request,'recepcion/list.html',{'res_today':res_today})

def recepcionentrega(request,id_R):
    reserva=get_object_or_404(Reservas,pk=id_R)
    return render(request,'recepcion/detail.html',{'reserva':reserva})

def recepcionconfirm(request,id_R):
    reserva=get_object_or_404(Reservas,pk=id_R)
    reserva.status="Encurso"
    recurso=reserva.recursos
    recurso.status="EnUso"
    recurso.save()
    reserva.save()
    return redirect('polireserva:recepcionlist')

def devolucion(request,id_R):
    reserva=get_object_or_404(Reservas,pk=id_R)
    date=datetime.now()
    if request.method == 'POST':
        form = DevolucionForm(request.POST)
        if form.is_valid():
          a=form.cleaned_data.get("man")
          if(a):
              recurso = reserva.recursos
              reserva.status = 'FIN'
              recurso.status = 'Disponible'
              reserva.save()
              recurso.save()
              return redirect('polireserva:devaman',reserva.id_R)
          else:
              recurso=reserva.recursos
              reserva.status='FIN'
              recurso.status='Disponible'
              reserva.save()
              recurso.save()
        return redirect('../../')
    else:
        form = DevolucionForm()
    return render(request,'recepcion/devolucion.html',{'reserva':reserva,
                                                     'form':form,
                                                     'date':date})



def devaman(request,id_R):
    reserva=get_object_or_404(Reservas,pk=id_R)
    date=datetime.now()
    if request.method == 'POST':
        form = DevMantenimientoForm(request.POST)
        if form.is_valid():
          new_man=form.save(commit=False)
          new_man.date_c=date.date()
          new_man.kindM='COR'
          new_man.recurso=reserva.recursos
          new_man.estado='Enespera'
          new_man.user=request.user
          new_man.date_c=date.date()
          new_man.save()
        return redirect('../../')
    else:
        form = DevMantenimientoForm()
    return render(request,'recepcion/amantenimiento.html',{'reserva':reserva,
                                                     'form':form,
                                                     'date':date})



@login_required(login_url='login/')
@has_permission_decorator('can_list_tdr')
def tdrlist(request):
    all_tdr = TdRecurso.objects.all().order_by('description')
    return render(request, 'tdr/list.html', {'all_tdr': all_tdr})


@login_required(login_url='login/')
@has_permission_decorator('can_list_tdr')
def tdrdetail(request, id_tdr):
    tdr = get_object_or_404(TdRecurso, pk=id_tdr)
    all_recursos = Recurso.objects.filter(id_tdr=tdr).order_by('name_r')
    return render(request, 'tdr/detail.html', {'tdr': tdr, 'all_recursos':all_recursos})


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
    messages.success(request, "El recurso fue eliminado exitosamente")
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
    messages.success(request, "El tipo de recurso fue eliminado exitosamente")
    return redirect('polireserva:tdrlist')


@login_required(login_url='login/')
@has_permission_decorator('can_add_tdr')
def newtdr(request):
    if request.method == 'POST':
        form = TdRecursoFillForm(request.POST)
        if form.is_valid():
            new_tdr = form.save(commit=False)
            new_tdr.save()
            messages.success(request, "El tipo de recurso fue agregado exitosamente")
            return redirect('polireserva:tdrlist')
    else:
        form = TdRecursoFillForm()
    return render(request, 'tdr/tdrfill.html', {'form': form})


## METODOS DE RESERVA ## cjba
@login_required(login_url='login/')
@has_permission_decorator('can_list_reserva')
def reservalist(request):
    all_reservas = Reservas.objects.all().order_by('date_i')
    return render(request, 'reservas/listareservas.html', {'all_reservas': all_reservas, 'titulo':'Reservas'})


@login_required(login_url='login/')
def misreservas(request):
    mis_reservas = Reservas.objects.filter(user=request.user).order_by('date_i')
    return render(request, 'reservas/listareservas.html', {'all_reservas': mis_reservas, 'titulo':'Mis Reservas'})


@login_required(login_url='login/')
def reservadetail(request, id_R):
    reserva = get_object_or_404(Reservas, pk=id_R)
    recurso = reserva.recursos
    return render(request, 'reservas/reservasdetail.html', {'reserva': reserva, 'recursos':recurso})

import datetime
@login_required(login_url='login/')
@has_permission_decorator('can_add_reserva')
def newreserva(request):
    if request.method == 'POST':
        form = ReservasForm(request.POST)
        if form.is_valid():
            new_reserva = form.save(commit=False)
            new_reserva.user = request.user
            #reservas = Reservas.objects.filter()
            new_reserva.save()
            form.save_m2m()
            recurso=form.cleaned_data.get('recursos')
            messages.success(request, "La reserva fue agregada exitosamente")
            if recurso.status == 'Mantenimiento':
                messages.warning(request, "El recurso seleccionado se encuentra actualmente en mantenimiento. Puede modificar su reserva si lo desea")
            return redirect('polireserva:reservadetail',new_reserva.id_R)
    else:
        form = ReservasForm()
    return render(request, 'reservas/newreserva.html', {'form': form, 'titulo':'Nueva Reserva', 'accion': 'Guardar'})


@login_required(login_url='login/')
@has_permission_decorator('can_modify_reserva')
def updatereserva(request, id_R=None):
    instance = get_object_or_404(Reservas, pk=id_R)
    form = ReservasForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        recurso=form.cleaned_data.get('recursos')
        messages.success(request, "Los cambios se guardaron exitosamente")
        if recurso.status == 'Mantenimiento':
            messages.warning(request, "El recurso seleccionado se encuentra actualmente en mantenimiento. Puede modificar su reserva si lo desea")
        return redirect('polireserva:reservadetail', instance.id_R)
    return render(request, 'reservas/newreserva.html', {'form': form, 'titulo':'Modificar Reserva', 'accion':'Modificar'})


@login_required(login_url='login/')
def deletereserva(request,id_R):
    reserva = get_object_or_404(Reservas, pk=id_R)
    return render(request,'reservas/deletereserva.html', {'reserva':reserva})

@login_required(login_url='login/')
def deletereservaconfirm(request,id_R):
    reserva = get_object_or_404(Reservas, pk=id_R)
    reserva.delete()
    messages.success(request, "La reserva fue eliminada exitosamente")
    return redirect('polireserva:misreservas')


@login_required(login_url='login/')
@has_permission_decorator('can_add_recurso')
def newrecurso(request, id_tdr):
    tdr = get_object_or_404(TdRecurso, pk=id_tdr)
    if request.method == 'POST':
        form = RecursoFillForm(request.POST)
        if form.is_valid():
            new_r = form.save(commit=False)
            new_r.id_tdr = tdr
            new_r.save()
            messages.success(request, "El recurso fue agregado exitosamente")
            return redirect('../')
    else:
        form = RecursoFillForm()
    return render(request, 'tdr/recursofill.html', {'form': form,
                                                    'tdr': tdr})


