from django.urls import path

from . import views

 

urlpatterns = [
  path('add-empresa/', views.add_empresa, name='add-empresa'),
  path('empresa-detail/<int:id>', views.empresa_detail, name='empresa-detail'),
  path('desativar-empresa/<int:id>/', views.desativar_empresa, name='desativar-empresa'),
  path('ativar-empresa/<int:id>/', views.ativar_empresa, name='ativar-empresa'),
]