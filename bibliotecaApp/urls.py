from django.urls import path

from . import views

 

urlpatterns = [

  path('', views.index, name='home'),
  path('add-livro/', views.add_product, name='add-livro'),
  path('delete-livro/<int:id>', views.delete_product, name='delete-livro'),
  path('livro-detail/<int:id>', views.product_detail, name='livro-detail')

]