from django.contrib import admin
from.models import Livro
from.models import Genero
# from.models import Genero

class LivrosAdmin(admin.ModelAdmin):
    list_display=['name', 'author','qtd', 'in_stock'] 
    list_filter=['in_stock']
    search_fields = ['name']

  
admin.site.register(Livro, LivrosAdmin)
admin.site.register(Genero)

# Register your models here.

