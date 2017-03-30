from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

class Usuario (AbstractBaseUser, Permis):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=True)
    lastname = models.CharField(max_length=30, blank=True)
    cin = models.IntegerField
    ladder = models.CharField(max_length=30, blank=True)
    phone = models.CharField(max_length=10, blank=True)
    email = models.EmailField

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()