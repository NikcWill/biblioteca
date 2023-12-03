from django.db import models
from empresa.models import Empresas
from accounts.models import CustomUser

class Genero(models.Model):
    cod = models.IntegerField(unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresas, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Gênero'
        verbose_name_plural = 'Gêneros'

class Livro(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresas, on_delete=models.CASCADE)
    cod = models.IntegerField(unique=True)
    name = models.CharField(max_length=255, blank=False)
    genery = models.ForeignKey(Genero, on_delete=models.CASCADE, blank=True)
    pg = models.IntegerField()
    picture = models.ImageField(blank=True)
    author = models.CharField(max_length=255)
    qtd = models.IntegerField()
    created_at = models.DateTimeField()
    in_stock = models.BooleanField(default=False)
    emprestado = models.IntegerField(default=0)

    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Livro'
        verbose_name_plural = 'Livros'
