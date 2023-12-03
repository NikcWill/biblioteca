from django.urls import path

from . import views

 

urlpatterns = [
  path('add-cliente/', views.add_cliente, name='add-cliente'),
  path('clientes/', views.clientes, name='clientes'),
  path('emprestados-livros/', views.emprestados_livros, name='emprestados-livros'),
  path('cliente-detail/<int:id>', views.cliente_detail, name='cliente-detail'),
  path('desativar-cliente/<int:id>', views.desativar_cliente, name='desativar-cliente'),
  path('ativar-cliente/<int:id>', views.ativar_cliente, name='ativar-cliente'),
  path('historico-cliente/<int:id>', views.historico_cliente, name='historico-cliente'),
  path('devolver-livro/<int:emprestimo_id>/', views.devolver_livro, name='devolver-livro'),
  path('add-emprestimo/', views.add_emprestimo, name='add-emprestimo'),
  path('selecionar_cliente/', views.selecionar_cliente, name='selecionar-cliente'),
  path('deletar_emprestimo/<int:emprestimo_id>/', views.deletar_emprestimo, name='deletar_emprestimo'),
]