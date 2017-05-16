
# Register your models here.

from django.contrib import admin
from .models import Usuario
from .models import TdRecurso
from .models import Recurso
from .models import Reserva
from .models import Mantenimiento
from .models import RecursoReserva
from .forms import TdRecursoForm
from .forms import RecursoForm
from .forms import ReservaForm
from .forms import RecursoReserva
from .forms import MantenimientoForm


class UsuarioAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {'fields': ('cin', 'ladder', 'user')}),
    )
    #fields = ('cin', 'ladder', 'user')
    form = TdRecursoForm

    list_display = ('cin', 'user')
    list_filter = ('cin',)
    search_fields = ('name', 'lastname')
    ordering = ('cin',)


admin.site.register(Usuario, UsuarioAdmin)


class TdRecursoAdmin(admin.ModelAdmin):
    '''
    actions over admin
    '''
    fields = ('id_tdr', 'description')
    ##query result for cont



    form = TdRecursoForm

    list_display = ('id_tdr', 'description')
    list_filter = ('id_tdr', 'description')
    search_fields = ('description',)
    ordering = ('id_tdr',)


admin.site.register(TdRecurso, TdRecursoAdmin)

class RecursoAdmin(admin.ModelAdmin):
    '''
    actions over admin
    '''
    
    fieldsets = ((None, {'fields': ('id_r', 'name_r', 'id_tdr', 'description', 'status', 'date_c', 'date_m')}),)

    form = RecursoForm

    list_display = ('id_r', 'id_tdr', 'name_r')
    list_filter = ('id_tdr', 'id_r')
    search_fields = ('name_r',)
    ordering = ('id_tdr',)


admin.site.register(Recurso, RecursoAdmin)


class ReservaAdmin(admin.ModelAdmin):

    fieldsets = ((None, {'fields' : ('id_R', 'tdr', 'user', 'status', 'obs', 'date_i', 'date_f')}),
    )

    form = ReservaForm

    list_display = ('id_R', 'user', 'status',)
    list_filter = ('status',)
    search_fields = ('id_R', 'status',)
    ordering = ('id_R',)

admin.site.register(Reserva, ReservaAdmin)

class RecursoReservaAdmin(admin.ModelAdmin):

    fieldsets = ((None, {'fields' : ('id_RR', 'id_reserva', 'id_recurso')}),
    )

    form = ReservaForm

    list_display = ('id_RR', 'id_reserva', 'id_recurso',)
    list_filter = ('id_reserva',)
    search_fields = ('id_reserva', 'id_recurso',)
    ordering = ('id_RR',)

admin.site.register(RecursoReserva, RecursoReservaAdmin)


class MantenimientoAdmin(admin.ModelAdmin):

    fieldsets = ((None, {'fields' : ('id_M', 'user', 'recurso', 'kindM', 'reason', 'report', 'date_c')}),
    )

    form = MantenimientoForm

    list_display = ('id_M', 'user',)
    list_filter = ('reason',)
    search_fields = ('id_M', 'user',)
    ordering = ('id_M',)

admin.site.register(Mantenimiento, MantenimientoAdmin)

