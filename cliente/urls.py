from django.urls import path

from . import views

 

urlpatterns = [
  path('add-cliente/', views.add_cliente, name='add-cliente'),
  path('add-emprestimo/', views.add_emprestimo, name='add-emprestimo'),
  # path('search-cliente/', views.search_cliente, name='search-cliente'),
  # path('cliente-detail/<int:id>', views.cliente_detail, name='cliente-detail')
]