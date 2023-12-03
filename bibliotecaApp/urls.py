from django.urls import path

from . import views

 

urlpatterns = [
    path('', views.index, name='home'),
    path('search-livros/', views.search_livros, name='search-livros'),
    path('search-livros-emprestados/', views.search_livros_emprestados, name='search-livros-emprestados'),
    path('add-livro/', views.add_livro, name='add-livro'),
    path('add-genero/', views.add_genero, name='add-genero'),
    path('delete-genero/<int:id>', views.delete_genero, name='delete-genero'),
    path('livros-emprestados/', views.livros_emprestados, name='livros-emprestados'),
    path('delete-livro/<int:id>', views.delete_livro, name='delete-livro'),
    path('desativar-livro/<int:id>', views.desativar_livro, name='desativar-livro'),
    path('ativar-livro/<int:id>', views.ativar_livro, name='ativar-livro'),
    path('livro-detail/<int:id>', views.livro_detail, name='livro-detail')
]