from attr.filters import exclude

from django import forms
from .models import *
from django.contrib.auth.models import User
from datetimewidget.widgets import DateTimeWidget


class TdRecursoForm(forms.ModelForm):
    class Meta:
        model = TdRecurso
        fields = ('id_tdr', 'description')


class TdRecursoFillForm(forms.ModelForm):
    description = forms.CharField(max_length=25, label="Nombre del tipo de Recurso",
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'descripciontdr'}))

    class Meta:
        model = TdRecurso
        fields = ('description',)


class RecursoForm(forms.ModelForm):
    class Meta:
        model = Recurso
        fields = ('name_r', 'status', 'date_c', 'date_m', 'description',)


class ReservasForm(forms.ModelForm):
    id_R = forms.IntegerField(label="ID", max_value=1000, widget=forms.HiddenInput, required=False)
    tdr = forms.ModelChoiceField(label="Tipo de recurso", queryset=TdRecurso.objects.all(), required=True,
                                 widget=forms.Select(attrs={'class': 'form-control', 'name': 'tdrselect'}))
    recursos = forms.ModelMultipleChoiceField(label="Recursos", queryset=Recurso.objects.all(), required=True,
                                              widget=forms.SelectMultiple(
                                                  attrs={'class': 'form-control', 'name': 'rselect'}))
    status = forms.ChoiceField(label="Tipo de recurso", choices=Reservas.STATUS_CHOICES, required=True, initial='',
                               widget=forms.Select(attrs={'class': 'form-control', 'name': 'statusselect'}))
    obs = forms.CharField(max_length=25, label="Observacion",
                          widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'reservaobs'}))
    date_i = forms.DateTimeField(label="Fecha", widget=DateTimeWidget(attrs={'class': 'form-control'}))
    date_f = forms.DateTimeField(label="Fecha", widget=DateTimeWidget(attrs={'class': 'form-control'}))

    class Meta:
        model = Reservas
        fields = ('tdr', 'recursos', 'status', 'obs', 'date_i', 'date_f')
        dateTimeOptions = {
            'format': 'dd/mm/yyyy HH:ii',
            'autoclose': True,
            'showMeridian': True
        }

        widgets = {
            # Use localization and bootstrap 3
            'date_i': DateTimeWidget(attrs={'id': "date_i", 'class': 'form-control'}, usel10n=True,
                                     bootstrap_version=3),
            'date_f': DateTimeWidget(attrs={'id': "date_f", 'class': 'form-control'}, usel10n=True, bootstrap_version=3)
        }
