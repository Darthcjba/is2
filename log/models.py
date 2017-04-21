from django.db import models

from django.contrib.auth.models import User

# Create your models here.
LADDER_CHOICES = (
    ('Usuario', 'Usuario normal'),
    ('Tecnico', 'Tecnico del sistema'),
    ('Recepcionista', 'Encargado de administrar reservas'),
    ('Invitado', 'Invitado'),
)

class Usuario (models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    cin = models.CharField(max_length=10, blank=True)
    ladder = models.CharField(max_length=30, blank=True, choices=LADDER_CHOICES)
    phone = models.CharField(max_length=10, blank=True)

