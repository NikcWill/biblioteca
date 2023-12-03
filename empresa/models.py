from django.db import models


class Empresas(models.Model):
    cod = models.IntegerField(unique=True)
    name = models.CharField(max_length=255, blank=False)
    cnpj = models.CharField(max_length=14)
    created_at = models.DateTimeField()
    active = models.BooleanField(default=False)
    total_usuarios = models.IntegerField(default=0)
    total_livros = models.IntegerField(default=0)
    total_livros_emprestados = models.IntegerField(default=0)
    total_clientes = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'