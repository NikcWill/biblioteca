from django.urls import path

from . import views

 

urlpatterns = [
  path('login/', views.user_login, name='login'),
  path('logout/', views.logout, name='logout'),
  path('add-user/', views.add_user, name='add-user'),
  path('desativar-user/<int:id>', views.desativar_user, name='desativar-user'),
  path('ativar-user/<int:id>', views.ativar_user, name='ativar-user'),
  path('desativar-superuser/<int:id>', views.desativar_superuser, name='desativar-superuser'),
  path('ativar-superuser/<int:id>', views.ativar_superuser, name='ativar-superuser'),
  path('user-detail/<int:id>', views.user_detail, name='user-detail'),
]