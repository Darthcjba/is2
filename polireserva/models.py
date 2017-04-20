from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class Usuario (models.Model):
    LADDER=(
        ('Usuario', 'Usuario normal'),
        ('Tecnico', 'Tecnico del sistema'),
        ('Recepcionista', 'Encargado de administrar reservas'),
        ('Invitado', 'Invitado'),
    )

    username = models.OneToOneField(User, on_delete=models.CASCADE)
    cin = models.PositiveIntegerField
    ladder = models.CharField(max_length=30, blank=True, choices=LADDER, name="ladder")
    phone = models.CharField(max_length=10, blank=True)


