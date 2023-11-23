from django.db import models
from django.contrib.auth.models import AbstractUser
from empresa.models import Empresas  

class Cargos(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'

class CustomUser(AbstractUser):
    cargo = models.ForeignKey(Cargos, on_delete=models.SET_NULL, null=True, blank=True)
    empresa = models.ForeignKey(Empresas, on_delete=models.SET_NULL, null=True, blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',  # Altere para o nome que preferir
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',  # Altere para o nome que preferir
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )
    def __str__(self):
        return self.username

