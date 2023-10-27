from django.urls import path

from . import views

 

urlpatterns = [

  path('', views.index, name='home'),
  path('add-livro/', views.add_livro, name='add-livro'),
  path('delete-livro/<int:id>', views.delete_livro, name='delete-livro'),
  path('livro-detail/<int:id>', views.livro_detail, name='livro-detail')

]