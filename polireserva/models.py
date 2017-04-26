from __future__ import unicode_literals

from django.db import models
from log.models import Usuario

# Create your models here.


class TdRecurso(models.Model):
    def __unicode__(self):
        return str(self.description)

    id_tdr = models.AutoField("Codigo del Tipo de Recurso", primary_key=True)
    description = models.CharField("Descripcion del Tipo de Recurso", max_length=30)

    def set_description(self, description):
        '''
        :return: 
        '''
        self.description = description
        return self

    def get_description(self):
        '''

        :return: 
        '''
        return self.description


class Recurso(models.Model):
    STATUS_CHOICES = (
        ('Disponible', 'Disponible'),
        ('EnUso', 'En Uso'),
        ('NoDisponible', 'No Disponible'),
        ('Mantenimiento', 'Mantenimiento')
    )

    id_r = models.AutoField("Codigo del item", primary_key=True)
    id_tdr = models.ForeignKey(TdRecurso)
    name_r = models.CharField("Nombre del item", max_length=30)
    description = models.CharField("Descripcion del item", max_length=50)
    status = models.CharField("Estado", choices=STATUS_CHOICES, default='Disponible', max_length=13)
    date_c = models.DateField("Fecha de submicion")
    date_m = models.DateField("Fecha de alteracion")

    def set_name_r(self, name):
        '''

        :param name: 
        :return: self.name_r
        '''
        self.name_r = name
        return self.name_r

    def set_descripton(self, description):
        '''

        :param description: 
        :return: 
        '''
        self.description = description
        return self

    def get_name_r(self):
        '''

        :return: 
        '''
        return self.name_r

    def get_description(self):
        '''
        :return: 
        '''
        return self.description

    def __str__(self):
        return self.name_r


class Reservas(models.Model):
    STATUS_CHOICES = (
        ('ACT', 'Activa'),
        ('CAN', 'Cancelada'),
        ('FIN', 'Finalizada')
    )

    id_R = models.AutoField(primary_key=True)

    user = models.ForeignKey(Usuario)
    tdr = models.ForeignKey(TdRecurso)
    recursos = models.ManyToManyField(Recurso)

    status = models.CharField(choices=STATUS_CHOICES, default='Activa', max_length=10)
    obs = models.CharField(max_length=100)  ##make it private possibly
    date_i = models.DateTimeField(auto_now=False, auto_now_add=False)
    date_f = models.DateTimeField(auto_now=False, auto_now_add=False)

    def _set_obs(self, obs):
        '''
        :param obs: 
        :return: 
        '''
        self._obs = obs
        return self._obs

    def _get_obs(self, obs):
        '''
        :param obs: 
        :return:
        '''

        return self._obs

    def set_date_i(self, date_i):
        '''
        :param date_i: 
        :return:
        '''
        self.date_i = date_i

        return self.date_i

    def set_date_f(self, date_f):
        self.date_f = date_f
        return self.date_f

    def get_date_i(self):
        return self.date_i

    def get_date_f(self):
        return self.date_f
