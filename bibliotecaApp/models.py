from django.db import models

# class Genero(models.Model):
#     name = models.CharField(max_length=255)

#     def __str__(self) -> str:
#         return self.name
    
#     class Meta:
#         verbose_name = 'Genero'
#         verbose_name_plural = 'Generos'

class Livro(models.Model):

   
    cod = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    # genery = models.ForeignKey(Genero, on_delete=models.CASCADE, blank=False)
    genery = models.CharField(max_length=255)
    pg = models.IntegerField()
    picture = models.ImageField(blank=False)
    author = models.CharField(max_length=255)
    qtd = models.IntegerField()
    name_sacado = models.CharField(max_length=255)

    created_at = models.DateTimeField()
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Livro'
        verbose_name_plural = 'Livros'