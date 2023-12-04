from django.shortcuts import render, HttpResponse, redirect
from django.contrib import auth, messages
from .models import Cargos, CustomUser
from django.contrib.auth.models import AbstractUser
from empresa.models import Empresas
from datetime import datetime, timedelta
from cliente.models import Emprestimo


def user_login(request):
    if request.method == 'POST':
        user = request.POST.get('username')
        password = request.POST.get('password')
        update_loan_days()
        
        userVerify = auth.authenticate(request, username=user, password=password)
        
        if userVerify is None:
            messages.info(request, 'Usuário ou senha incorretos!')
            return redirect('login')
        else:
            auth.login(request, userVerify)
        
            return redirect('home')
        
    else:
        return render(request, 'pages/login.html')


def update_loan_days():
    emprestimos = Emprestimo.objects.filter(devolvido=False)
    for emprestimo in emprestimos:
        data_atual = datetime.now().date()
        data_prev_devolucao = emprestimo.data_prev_devolucao.date()

        diferenca_dias = (data_prev_devolucao - data_atual).days
        emprestimo.dias_para_devolver = diferenca_dias
        emprestimo.save()

        return redirect('home')

def add_user(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        usuario = request.POST.get('usuario')
        email = request.POST.get('email')
        cargo_id = request.POST.get('cargo')  
        empresa_id = request.POST.get('empresa') 
        senha = request.POST.get('senha')
        senhaconfirma = request.POST.get('senha-repete')
        is_active = True

        cargo = Cargos.objects.get(pk=cargo_id)
        empresa = Empresas.objects.get(pk=empresa_id)
        
        user = CustomUser.objects.create_user(
        username=usuario, 
        email=email,
        password=senha, 
        first_name=name,
        is_active=is_active,
        cargo=cargo,  
        empresa=empresa  
        )

        return redirect('login')
    else:
        empresas = Empresas.objects.all()
        cargos = Cargos.objects.all()
        return render(request, 'pages/add-user.html', {'empresas': empresas, 'cargos': cargos})  
    
def logout(request):
  auth.logout(request)
  return redirect('login') 
    