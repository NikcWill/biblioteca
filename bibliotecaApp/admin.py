from django.contrib import admin
from.models import Livro
from.models import Genero
from empresa.models import Empresas
from cliente.models import Cliente, Emprestimo
from accounts.models import Cargos, CustomUser
# from.models import Genero

class LivrosAdmin(admin.ModelAdmin):
    list_display=['id','name', 'author','qtd', 'in_stock'] 
    list_filter=['in_stock']
    search_fields = ['name']

class EmpresasAdmin(admin.ModelAdmin):
    list_display=['id','name', 'cnpj','active', 'created_at'] 
    list_filter=['active']
    search_fields = ['name']

  
admin.site.register(Livro, LivrosAdmin)
admin.site.register(Genero)
admin.site.register(Empresas, EmpresasAdmin)
admin.site.register(Cargos)
admin.site.register(CustomUser)
admin.site.register(Cliente)
admin.site.register(Emprestimo)

# Register your models here.

