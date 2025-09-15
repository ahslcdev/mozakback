from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

from apps.base.models import BaseModel
from apps.usuarios.managers import UsuarioManager


class Usuario(AbstractUser, PermissionsMixin, BaseModel):
    data_nascimento = models.DateField(null=True, blank=True)

    objects = UsuarioManager()

    def __str__(self):
        return self.email
