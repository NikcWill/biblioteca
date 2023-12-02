from django.urls import path

from . import views

 

urlpatterns = [
    path('', views.index, name='home'),
    path('search-livros/', views.search_livros, name='search-livros'),
    path('search-livros-emprestados/', views.search_livros_emprestados, name='search-livros-emprestados'),
    path('add-livro/', views.add_livro, name='add-livro'),
    path('livros-emprestados/', views.livros_emprestados, name='livros-emprestados'),
    path('delete-livro/<int:id>', views.delete_livro, name='delete-livro'),
    path('livro-detail/<int:id>', views.livro_detail, name='livro-detail')
]