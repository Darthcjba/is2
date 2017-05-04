
from __future__ import unicode_literals

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import models
from django.contrib import messages


# Create your models here.

'''
class UsuarioManager(BaseUserManager):

    def create_user(self, email, name, lastname, ladder, cin, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email = UsuarioManager.normalize_email(email),
            name = name,
            lastname = lastname,
            ladder = ladder,
            cin = cin,
         )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, lastname, ladder, cin, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        u = self.create_user(email, name, lastname, ladder, cin, password=password)
        u.is_admin = True
        u.save(using=self._db)
        return u
'''


class Usuario(models.Model):

    def __unicode__(self):
        return str(self.user.username)


    user = models.ForeignKey(User)
    ladder = models.CharField("Cargo del Usuario en la Institucion", max_length=20)
    cin = models.CharField("Nro de Cedula de Identidad", primary_key=True, max_length=7)


    '''
    name = models.CharField(max_length=20, editable=True)
    lastname = models.CharField(max_length=20, editable=True)
    cin = models.CharField(max_length=7, primary_key=True)
    ladder = models.CharField(max_length=20)
    email = models.EmailField(('email address'), max_length=255,
                              unique=True)
    is_staff = models.BooleanField(
        ('staff status'), default=False, help_text=(
            'Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(('active'), default=True, help_text=(
        'Designates whether this user should be treated as '
        'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(('date joined'))
    '''




class TdRecurso(models.Model):

    def __unicode__(self):
        return str(self.description)

    id_tdr = models.IntegerField("Codigo del Tipo de Recurso", primary_key=True)
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


    def __unicode__(self):
        return str(self.name_r)

    STATUS_CHOICES = (
        ('Disponible', 'Disponible'),
        ('EnUso', 'EnUso'),
        ('NoDisponible', 'NoDisponible'),
        ('Mantenimiento', 'Mantenimiento')
    )


    id_r = models.IntegerField("Codigo del item", primary_key=True)
    id_tdr = models.ForeignKey(TdRecurso)
    name_r = models.CharField("Nombre del item", max_length = 30)
    description = models.CharField("Descripcion del item", max_length = 50)
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



class Reservas(models.Model):




    STATUS_CHOICES = (
        ('ACT', 'Activa'),
        ('CAN', 'Cancelada'),
        ('FIN', 'Finalizada')
    )

    id_R = models.IntegerField(primary_key=True)

    user = models.ForeignKey(Usuario)
    tdr = models.ForeignKey(TdRecurso)
    recursos = models.ManyToManyField(Recurso, validators=[])

    status = models.CharField(choices = STATUS_CHOICES, default = 'Activa', max_length = 10 )
    obs = models.CharField(max_length=100) ##make it private possibly
    date_i = models.DateTimeField( auto_now = False, auto_now_add = False)
    date_f = models.DateTimeField(auto_now=False, auto_now_add=False)


    '''def save(self, *args, **kwargs):

        recurso = Recurso.objects.get(id=self.recursos.)
        if recurso.status == 'Disponible':
            super(Reservas, self).save(*args, **kwargs)
        else:
            raise Exception('Not available', 'Fuck you')
    '''





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


class Mantenimiento(models.Model):

    KIND_CHOICES = (
        ('PRE', 'Preventivo'),
        ('COR', 'Correctivo')
    )

    id_M = models.IntegerField(primary_key=True)
    user = models.ForeignKey(Usuario)
    recurso = models.ForeignKey(Recurso)
    date_c = models.DateField("Fecha de submicion")
    kindM = models.CharField("Tipo de mantenimiento realizado", choices=KIND_CHOICES, default='Preventivo', max_length=10)
    reason = models.CharField("Razon del mantenimiento", max_length=200)
    report = models.CharField("Reporte de finalizacion", max_length=100)

    def get_report(self):
        '''
        get reporte
        :return: reporte
        '''
        return self.report

    def get_reason(self):
        '''
        get razon
        :return: razon
        '''
        return self.reason

    def get_date_c(self):

        '''
        get fecha
        :return: fecha
        '''
        return self.date_c

    def set_report(self, *args):
        '''
        set reporte
        :param args: 
        :return: 
        '''
        self.report = args
        return self.report

    def set_date_c(self, date):
        '''
        set fecha
        :param date: 
        :return: 
        '''
        self.date_c = date
        return self.date_c

    def set_reason(self, reason):
        '''
        set razon
        :param reason: 
        :return: 
        '''
        self.reason = reason
        return self.reason

