from django.contrib import admin
from.models import Livro
from.models import Genero
from empresa.models import Empresas
from cliente.models import Cliente, Emprestimo
from accounts.models import Cargos, CustomUser
from django.db.models import F
# from.models import Genero

class LivrosAdmin(admin.ModelAdmin):
    list_display=['id','name', 'author','qtd', 'in_stock', 'empresa'] 
    list_filter=['in_stock']
    search_fields = ['name']

class EmpresasAdmin(admin.ModelAdmin):
    list_display=['id','name', 'cnpj','active', 'created_at'] 
    list_filter=['active']
    search_fields = ['name']

class ClientesAdmin(admin.ModelAdmin):
    list_display=['id','name', 'cpf','active', 'empresa'] 
    list_filter=['active']
    search_fields = ['name']

class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'livro', 'data_emprestimo', 'devolvido']
    list_filter = ['devolvido']
    search_fields = ['cliente__name', 'livro__name']

    def delete_queryset(self, request, queryset):
        livro_count = {}
        cliente_count = {}

        for obj in queryset:
            livro = obj.livro
            cliente = obj.cliente

            livro_count[livro.id] = livro_count.get(livro.id, 0) + 1
            cliente_count[cliente.id] = cliente_count.get(cliente.id, 0) + 1

        for livro_id, count in livro_count.items():
            Livro.objects.filter(id=livro_id).update(emprestado=F('emprestado') - count)

        for cliente_id, count in cliente_count.items():
            Cliente.objects.filter(id=cliente_id).update(qtd_livros=F('qtd_livros') - count)

        super().delete_queryset(request, queryset)

admin.site.register(Emprestimo, EmprestimoAdmin)
admin.site.register(Livro, LivrosAdmin)
admin.site.register(Genero)
admin.site.register(Empresas, EmpresasAdmin)
admin.site.register(Cargos)
admin.site.register(CustomUser)
admin.site.register(Cliente, ClientesAdmin)



# Register your models here.

