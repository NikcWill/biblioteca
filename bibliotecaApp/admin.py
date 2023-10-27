from django.contrib import admin
from.models import Livro
from.models import Generos

class LivrosAdmin(admin.ModelAdmin):
    list_display=['name', 'author','qtd'] 
    list_filter=['name_sacado']
    search_fields = ['name']

  
admin.site.register(Livro, LivrosAdmin)
admin.site.register(Generos)

# Register your models here.

