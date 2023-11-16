from django.urls import path

from . import views

 

urlpatterns = [
  path('login/', views.user_login, name='login'),
  path('add-user/', views.add_user, name='add-user')
]