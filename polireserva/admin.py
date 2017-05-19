from django.contrib import admin

# Register your models here.
from .forms import TdRecursoForm
from .forms import RecursoForm
from .forms import ReservasForm
from .forms import MantenimientoForm
from .models import TdRecurso
from .models import Recurso
from .models import Reservas
from .models import Mantenimiento


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

    fieldsets = ((None, {'fields': ( 'name_r', 'id_tdr', 'description', 'status', 'date_c', 'date_m')}),)

    form = RecursoForm

    list_display = ('id_r', 'id_tdr', 'name_r')
    list_filter = ('id_tdr', 'id_r')
    search_fields = ('name_r',)
    ordering = ('id_tdr',)


admin.site.register(Recurso, RecursoAdmin)


class ReservasAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ('id_R', 'tdr', 'user', 'recursos', 'status', 'obs', 'date_i', 'date_f')}),
                 )

    form = ReservasForm

    list_display = ('id_R', 'user', 'status',)
    list_filter = ('status',)
    search_fields = ('id_R', 'status',)
    ordering = ('id_R',)


admin.site.register(Reservas, ReservasAdmin)


class MantenimientoAdmin(admin.ModelAdmin):

    fieldsets = ((None, {'fields' : ('user', 'recurso', 'kindM', 'reason', 'report', 'date_c')}),)

    form = MantenimientoForm

    list_display = ('id_M', 'user',)
    list_filter = ('reason',)
    search_fields = ('id_M', 'user',)
    ordering = ('id_M',)

admin.site.register(Mantenimiento, MantenimientoAdmin)
