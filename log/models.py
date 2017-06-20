from django.db import models

from django.contrib.auth.models import User

# Create your models here.
LADDER_CHOICES = (
    ('1', 'Invitado'),
    ('2', 'Alumno'),
    ('3', 'Auxiliar'),
    ('4', 'Profesor'),
    ('5', 'Director'),
)

class Usuario (models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    cin = models.CharField(max_length=10, blank=True)
    ladder = models.CharField(max_length=30, blank=True, choices=LADDER_CHOICES)
    phone = models.CharField(max_length=10, blank=True)

