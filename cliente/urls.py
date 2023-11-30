from django.urls import path

from . import views

 

urlpatterns = [
  path('add-cliente/', views.add_cliente, name='add-cliente'),
  path('clientes/', views.clientes, name='clientes'),
  # path('search-cliente/', views.search_cliente, name='search-cliente'),
  path('cliente-detail/<int:id>', views.cliente_detail, name='cliente-detail'),
  path('historico-cliente/<int:id>', views.historico_cliente, name='historico-cliente'),
  path('devolver-livro/<int:emprestimo_id>/', views.devolver_livro, name='devolver-livro'),
  path('add-emprestimo/', views.add_emprestimo, name='add-emprestimo'),
  path('selecionar_cliente/', views.selecionar_cliente, name='selecionar-cliente'),
]