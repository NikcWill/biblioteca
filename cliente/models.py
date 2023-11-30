from django.db import models
from bibliotecaApp.models import Livro
from empresa.models import Empresas
from accounts.models import CustomUser
from uuid import uuid4 


class Cliente(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresas, on_delete=models.CASCADE)
    cod = models.IntegerField(unique=True)
    name = models.CharField(max_length=255, blank=False)
    cpf = models.CharField(max_length=14)
    email = models.EmailField()
    created_at = models.DateTimeField()
    active = models.BooleanField(default=False)
    qtd_livros = models.IntegerField()

    def livros_emprestados(self):
        return Livro.objects.filter(emprestimo__cliente=self)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'


class Emprestimo(models.Model):
    cod = models.CharField(max_length=36, unique=True)  
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresas, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    data_emprestimo = models.DateTimeField()
    data_prev_devolucao = models.DateTimeField()
    data_devolucao = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Gere um UUID único ao salvar um novo objeto Emprestimo
        if not self.cod:
            self.cod = str(uuid4())
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cliente.name} - {self.livro.name}"

    class Meta:
        verbose_name = 'Empréstimo'
        verbose_name_plural = 'Empréstimos'
