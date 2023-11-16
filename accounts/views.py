from django.shortcuts import render, HttpResponse,redirect
from django.contrib import auth, messages
from django.contrib.auth.models import User
from random import randint

def user_login(request):

    if request.method == 'POST':
        user = request.POST.get('username')
        password = request.POST.get('password')
        

        userVerify = auth.authenticate(
            request, username=user, password=password)
        
        if userVerify == None:
            messages.info(request, 'Usuário ou senha incorretos seu tanso!')
            return redirect('login')
        else:
            auth.login(request, userVerify)
            return redirect('home')
    else:

        return render(request,'pages/login.html')

def add_user(request ):
  if request.method == 'POST':

    name = request.POST.get('name')
    usuario = request.POST.get('usuario')
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    senhaconfirma = request.POST.get('senha-repete')
    cod = randint(100, 10000)
    is_active = True

    User.objects.create_user(
      username=usuario, email=email,
      password=senha, first_name=name
    )
    return redirect('login')
    
  else:
    return render(request,'pages/add-user.html')  
 
    