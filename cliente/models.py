from django.db import models
from bibliotecaApp.models import Livro
from empresa.models import Empresas
from accounts.models import CustomUser


class Cliente(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresas, on_delete=models.CASCADE)
    cod = models.IntegerField(unique=True)
    name = models.CharField(max_length=255, blank=False)
    cpf = models.CharField(max_length=14)
    email = models.EmailField()
    created_at = models.DateTimeField()
    active = models.BooleanField(default=False)

    def livros_emprestados(self):
        return Livro.objects.filter(emprestimo__cliente=self)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'


class Emprestimo(models.Model):
    cod = models.IntegerField(unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresas, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    data_emprestimo = models.DateTimeField()
    data_prev_devolucao = models.DateTimeField()
    data_devolucao = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.cliente.name} - {self.livro.name}"
