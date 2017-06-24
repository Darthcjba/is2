from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import Table, TableStyle
from rolepermissions.decorators import has_permission_decorator
from rolepermissions.roles import get_user_roles, assign_role, remove_role, clear_roles

from rolepermissions.roles import get_user_roles, assign_role
from django.http import HttpResponse
from log.models import Usuario
from .forms import *
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import date,datetime
from django.core.mail import send_mail
from django.core import serializers
import json
from django.conf import settings
from io import BytesIO
from reportlab.pdfgen import canvas
from django.views.generic import View


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
    all_tdr = TdRecurso.objects.all().order_by('description')
    all_res=Reservas.objects.all()
    all_rec=Recurso.objects.all()
    num = len(all_tdr)
    max=len(all_res)
    sum = [None] * len(all_tdr)
    times= [0] * len(all_tdr)
    plus=[0]*len(all_rec)
    names=[None] * len(all_tdr)

    for i in range(num):
        tdr = all_tdr[i].id_tdr
        all_recursos = Recurso.objects.filter(id_tdr=tdr).order_by('name_r')
        tam = len(all_recursos)
        sum[i] = tam
        names[i] = all_tdr[i].description

    for j in range(max):
        p=all_res[j].tdr_id
        tipoder=TdRecurso.objects.get(pk=p)
        for i in range(num):
            if (names[i]==tipoder.description):
                times[i]=times[i]+1
        for q in range(len(all_rec)):
            if (all_rec[q]==all_res[j].recursos):
                plus[q]=plus[q]+1
    return render(request, 'modulos/modulo_dashboard.html',{'names':json.dumps(names),
                                                            'data':json.dumps(sum),
                                                            'times':json.dumps(times),
                                                            'all_rec':all_rec,
                                                            'plus':plus})


@login_required(login_url='login/')
@has_permission_decorator('can_list_usuarios')
def userlist(request):
    all_user = Usuario.objects.all().order_by('username')
    return render(request,'usuarios/list.html',{'all_user':all_user})


@login_required(login_url='login/')
@has_permission_decorator('can_delete_usuario')
def deleteusuario(request,username_id):
    user = User.objects.get(id=username_id)
    return render(request, 'usuarios/deleteusuario.html', {'user': user})


@login_required(login_url='login/')
@has_permission_decorator('can_delete_usuario')
def deleteusuarioconfirm(request,username_id):
    user = User.objects.get(id=username_id)
    user.delete()
    messages.success(request, "El usuario fue eliminado exitosamente")
    return redirect('polireserva:userlist')


@login_required(login_url='login/')
@has_permission_decorator('can_access_admin')
def rolelist(request,username_id):
    user= User.objects.get(id=username_id)
    roles = get_user_roles(user)
    return render(request,'usuarios/roles.html',{'user':user,
                                                 'roles':roles})

@login_required(login_url='login/')
@has_permission_decorator('can_assign_role')
def roleassing(request,username_id):
    user=User.objects.get(id=username_id)
    return render(request, 'usuarios/addrole.html',{'user':user})


@login_required(login_url='login/')
@has_permission_decorator('can_assign_role')
def roleassignation(request,username_id,string):
    user = User.objects.get(id=username_id)
    assign_role(user,string)
    messages.success(request, "Se agrego el rol "+string)
    return redirect('polireserva:roleslist',username_id)


@login_required(login_url='login/')
@has_permission_decorator('can_assign_role')
def roleclear(request,username_id):
    user = User.objects.get(id=username_id)
    clear_roles(user)
    messages.success(request, "Se limpiaron los roles para este usuario")
    return redirect('polireserva:roleslist',username_id)


@login_required(login_url='login/')
@has_permission_decorator('can_access_mantenimiento')
def mantenimientolist(request):
    all_man = Mantenimiento.objects.filter(estado="Encurso")
    all_need = Mantenimiento.objects.filter(estado="Enespera")
    return render(request,'mantenimiento/list.html',{'all_man': all_man, 'all_need':all_need})


@login_required(login_url='login/')
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


@login_required(login_url='login/')
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

@login_required(login_url='login/')
def amantenimiento(request,id_M):
    man = get_object_or_404(Mantenimiento,pk=id_M)
    rec = man.recurso
    return render(request, 'mantenimiento/detail.html', {'man': man,
                                                       'rec': rec})

@login_required(login_url='login/')
def enviarman(request,id_M):
    man = get_object_or_404(Mantenimiento,pk=id_M)
    man.estado="Encurso"
    rec=man.recurso
    rec.status="Mantenimiento"
    rec.save()
    man.save()
    return redirect('polireserva:mantenimientolist')


@login_required(login_url='login/')
@has_permission_decorator('can_access_recepcion')
def recepcionlist(request):
    d=date.today()
    res_today=[]
    all_res=Reservas.objects.all()
    for res in all_res:
        if res.date_i.date() == d :
            res_today.append(res)
    return render(request,'recepcion/list.html',{'res_today':res_today})


@login_required(login_url='login/')
@has_permission_decorator('can_access_recepcion')
def recepcionentrega(request,id_R):
    reserva=get_object_or_404(Reservas,pk=id_R)
    return render(request,'recepcion/detail.html',{'reserva':reserva})


@login_required(login_url='login/')
@has_permission_decorator('can_access_recepcion')
def recepcionconfirm(request,id_R):
    reserva=get_object_or_404(Reservas,pk=id_R)
    reserva.status="Encurso"
    recurso=reserva.recursos
    recurso.status="EnUso"
    recurso.save()
    reserva.save()
    return redirect('polireserva:recepcionlist')


@login_required(login_url='login/')
def devolucion(request,id_R):
    reserva=get_object_or_404(Reservas,pk=id_R)
    date=timezone.now()
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


@login_required(login_url='login/')
def devaman(request,id_R):
    reserva=get_object_or_404(Reservas,pk=id_R)
    date=timezone.now()
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
    return render(request, 'reservas/listareservas.html', {'all_reservas': all_reservas, 'titulo':'Reservas del Sistema'})


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
            rdate_i = form.cleaned_data.get("date_i")
            rdate_f = form.cleaned_data.get("date_f")
            rtdr = form.cleaned_data.get("tdr")
            rrecursos = form.cleaned_data.get("recursos")
            #reservas = Reservas.objects.filter()
            reservas = Reservas.objects.filter(recursos=rrecursos, date_i__day=rdate_i.day)
            new_reserva = Reservas(user=request.user, tdr=rtdr, recursos=rrecursos, status='Activa', obs='Ninguna', date_i=rdate_i, date_f=rdate_f)

            if not reservas:
                print 'entra en None'
                new_reserva.save()
            else:
                print 'entra en el else de if not'
                for reserva in reservas:
                    print 'if not {} <= {} <= {}: '.format(reserva.date_i.hour,rdate_i.hour,reserva.date_f.hour)
                    if not reserva.date_i.hour <= rdate_i.hour <= reserva.date_f.hour:
                        print 'if not {} <= {} <= {}: '.format(reserva.date_i.hour, rdate_f.hour, reserva.date_f.hour)
                        if not reserva.date_i.hour <= rdate_f.hour <= reserva.date_f.hour:
                            new_reserva.save()
                        else:
                            print 'entra en el else 1'
                            usuario_bd = Usuario.objects.get(username=reserva.user)
                            usuario_rq = Usuario.objects.get(username=new_reserva.user)
                            if usuario_rq.ladder == usuario_bd.ladder:
                                messages.warning(request,"El recurso seleccionado se encuentra actualmente en reservado. Puede modificar su reserva si lo desea")
                                return render(request, 'reservas/newreserva.html',
                                              {'form': form, 'titulo': 'Nueva Reserva', 'accion': 'Guardar'})
                            if usuario_rq.ladder > usuario_bd.ladder:
                                print 'request > db'
                                print usuario_bd.username.id
                                Reservas.objects.get(id_R=reserva.id_R ).delete()
                                #mandando mails
                                print usuario_bd.username.email
                                send_mail(
                                   'Notificacion de Polireserva',
                                   'Aviso para ' + usuario_bd.username.first_name + ' ' + usuario_bd.username.last_name + '! Un usuario con mayor prioridad ha reservado dentro del mismo horario que usted. Por favor seleccione otro recurso.',
                                   'polireservais2@gmail.com',
                                   [usuario_bd.username.email],
                                   fail_silently=False,
                                )
                                new_reserva.save()

                    else:
                        print 'entra en el else 2'
                        usuario_bd = Usuario.objects.get(username=reserva.user)
                        usuario_rq = Usuario.objects.get(username=new_reserva.user)
                        if usuario_rq.ladder == usuario_bd.ladder:
                            messages.warning(request,"El recurso seleccionado se encuentra actualmente en reservado. Puede modificar su reserva si lo desea")
                            return render(request, 'reservas/newreserva.html',
                                          {'form': form, 'titulo': 'Nueva Reserva', 'accion': 'Guardar'})
                        if usuario_rq.ladder > usuario_bd.ladder:
                            print usuario_bd.username.id
                            Reservas.objects.get(id_R=reserva.id_R).delete()
                            #mandando mails
                            print usuario_bd.username.email
                            send_mail(
                               'Notificacion de Polireserva',
                               'Aviso para ' + usuario_bd.username.first_name + ' ' + usuario_bd.username.last_name + '! Un usuario con mayor prioridad ha reservado dentro del mismo horario que usted. Por favor seleccione otro recurso.',
                               'polireservais2@gmail.com',
                               [usuario_bd.username.email],
                               fail_silently=False,
                            )
                            new_reserva.save()
                # new_reserva.save()


            form.save_m2m()
            recurso=form.cleaned_data.get('recursos')
            messages.success(request, "La reserva fue agregada exitosamente")
            if recurso.status == 'Mantenimiento':
                messages.warning(request, "El recurso seleccionado se encuentra actualmente en mantenimiento. Puede modificar su reserva si lo desea")
            return redirect('polireserva:reservadetail',new_reserva.id_R)
            #return redirect('/')
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

class ReporteRecursosPDF(View):

    def cabecera(self,pdf):
        #Utilizamos el archivo logo
        archivo_imagen = settings.MEDIA_ROOT +'/images/bg_poli.jpeg'
        pdf.drawImage(archivo_imagen, 40, 750, 120, 90,preserveAspectRatio=True)
        pdf.setFont("Helvetica", 16)
        pdf.drawString(230, 790, u"POLIRESERVAS")
        pdf.setFont("Helvetica", 14)
        pdf.drawString(200, 770, u"REPORTE DE RECURSOS")

    def get(self, request, *args, **kwargs):
        #Indicamos el tipo de contenido a devolver, en este caso un pdf
        response = HttpResponse(content_type='application/pdf')
        #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
        buffer = BytesIO()
        #Canvas nos permite hacer el reporte con coordenadas X y Y
        pdf = canvas.Canvas(buffer)
        self.cabecera(pdf)
        y=550
        self.tabla(pdf,y)
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

    def tabla(self, pdf, y):
        # Creamos una tupla de encabezados para neustra tabla
        encabezados = ('Recurso', 'Tipo de Recurso', 'Estado')
        all_rec=Recurso.objects.all()
        # Creamos una lista de tuplas que van a contener a las personas
        detalles = [(rec.name_r, rec.id_tdr, rec.status) for rec in all_rec]
        detalle_orden = Table([encabezados] + detalles, colWidths=[5 * cm, 5 * cm, 5 * cm])
        # Aplicamos estilos a las celdas de la tabla
        detalle_orden.setStyle(TableStyle(
            [
                # La primera fila(encabezados) va a estar centrada
                ('ALIGN', (0, 0), (2, 0), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
            ]
        ))
        detalle_orden.wrapOn(pdf, 800, 600)
        detalle_orden.drawOn(pdf, 120, y)

class ReporteReservaPDF(View):

    def cabecera(self,pdf):
        #Utilizamos el archivo logo
        archivo_imagen = settings.MEDIA_ROOT +'/images/bg_poli.jpeg'
        pdf.drawImage(archivo_imagen, 40, 750, 120, 90,preserveAspectRatio=True)
        pdf.setFont("Helvetica", 16)
        pdf.drawString(230, 790, u"POLIRESERVAS")
        pdf.setFont("Helvetica", 14)
        pdf.drawString(200, 770, u"REPORTE DE RESERVAS")

    def get(self, request, *args, **kwargs):
        #Indicamos el tipo de contenido a devolver, en este caso un pdf
        response = HttpResponse(content_type='application/pdf')
        #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
        buffer = BytesIO()
        #Canvas nos permite hacer el reporte con coordenadas X y Y
        pdf = canvas.Canvas(buffer)
        self.cabecera(pdf)
        y=420
        self.tabla(pdf,y)
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

    def tabla(self, pdf, y):
        # Creamos una tupla de encabezados para neustra tabla
        encabezados = ('Recurso', 'Estado', 'Fecha inicio','Fecha fin','Usuario')
        all_res=Reservas.objects.all()
        # Creamos una lista de tuplas que van a contener a las personas
        detalles = [(res.recursos, res.status, res.date_i, res.date_f, res.user) for res in all_res]
        detalle_orden = Table([encabezados] + detalles, colWidths=[4 * cm, 2 * cm, 5 * cm, 5 * cm, 4 * cm])
        # Aplicamos estilos a las celdas de la tabla
        detalle_orden.setStyle(TableStyle(
            [
                # La primera fila(encabezados) va a estar centrada
                ('ALIGN', (0, 0), (4, 0), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
            ]
        ))
        detalle_orden.wrapOn(pdf, 600, 600)
        detalle_orden.drawOn(pdf, 15, y)
