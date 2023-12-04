from django.shortcuts import render, HttpResponse, redirect
from django.contrib import auth, messages
from .models import Cargos, CustomUser
from django.contrib.auth.models import AbstractUser
from empresa.models import Empresas
from datetime import datetime, timedelta
from cliente.models import Emprestimo, Cliente
from bibliotecaApp.models import Livro, Genero
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect



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
    
@login_required(redirect_field_name='login')
def add_user(request):
    if not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para adicionar um usuário.', extra_tags='warning')
        return redirect('home')
    
    total_livros_cadastrados = Livro.objects.count()
    total_livros_emprestados = Emprestimo.objects.filter(devolvido=False).count()
    total_clientes_cadastrados = Cliente.objects.count()

    empresas = Empresas.objects.all()
    cargos = Cargos.objects.all()
    users = CustomUser.objects.all()

    if not empresas.exists():
        messages.warning(request, 'Não existem empresas cadastradas. Por favor, adicione uma empresa antes de criar usuários.', extra_tags='info')
        return redirect('add-empresa')
    
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
        
        messages.success(request, 'Usuário adicionado com sucesso!', extra_tags='success')
        return redirect('add-user')  
    
    return render(request, 'pages/add-user.html', {
        'empresas': empresas,
        'cargos': cargos,
        'users': users,
        'total_livros_cadastrados': total_livros_cadastrados,
        'total_livros_emprestados': total_livros_emprestados,
        'total_clientes_cadastrados': total_clientes_cadastrados,
    })
    
def logout(request):
  auth.logout(request)
  return redirect('login')

@login_required(redirect_field_name='login')
def desativar_user(request, id):
    user_to_deactivate = get_object_or_404(CustomUser, id=id)

    if request.user.id == user_to_deactivate.id:
        messages.error(request, 'Você não pode desativar a si mesmo.', extra_tags='warning')
        return redirect('add-user')

    if not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para desativar um usuário.', extra_tags='warning')
        return redirect('home')

    user_to_deactivate.is_active = False
    user_to_deactivate.save()

    messages.success(request, 'Usuário desativado com sucesso.', extra_tags='success')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER') + '?desativar_user=true')

@login_required(redirect_field_name='login')
def ativar_user(request, id):
    user_to_activate = get_object_or_404(CustomUser, id=id)

    if request.user.id == user_to_activate.id:
        messages.error(request, 'Você não pode ativar a si mesmo.', extra_tags='warning')
        return redirect('add-user')

    if not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para ativar um usuário.', extra_tags='warning')
        return redirect('home')

   
    user_to_activate.is_active = True
    user_to_activate.save()

    messages.success(request, 'Usuário ativado com sucesso.', extra_tags='success')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER') + '?ativar_user=true')

@login_required(redirect_field_name='login')
def desativar_superuser(request, id):
    user_to_deactivate = get_object_or_404(CustomUser, id=id)

  
    if request.user.id == user_to_deactivate.id:
        messages.error(request, 'Você não pode desativar a si mesmo.', extra_tags='warning')
        return redirect('add-user')

    if not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para desativar um usuário.', extra_tags='warning')
        return redirect('home')

 
    if user_to_deactivate.is_superuser:
        user_to_deactivate.is_superuser = False  
        user_to_deactivate.save()

    user_to_deactivate.is_active = False
    user_to_deactivate.save()

    messages.success(request, 'Usuário desativado com sucesso.', extra_tags='success')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER') + '?desativar_user=true')

@login_required(redirect_field_name='login')
def ativar_superuser(request, id):
    user_to_activate = get_object_or_404(CustomUser, id=id)

    if request.user.id == user_to_activate.id:
        messages.error(request, 'Você não pode ativar a si mesmo.', extra_tags='warning')
        return redirect('add-user')

    if not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para ativar um usuário.', extra_tags='warning')
        return redirect('home')

    if not user_to_activate.is_superuser:
        user_to_activate.is_superuser = True
        user_to_activate.save()

    messages.success(request, 'Usuário ativado com sucesso.', extra_tags='success')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER') + '?ativar_user=true')

@login_required(redirect_field_name='login')
def user_detail(request, id):
    user = get_object_or_404(CustomUser, id=id)
    empresas = Empresas.objects.all()
    cargos = Cargos.objects.all()

    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.first_name = request.POST.get('first_name')
        user.email = request.POST.get('email')
        user.empresa_id = request.POST.get('empresa')
        user.cargo_id = request.POST.get('cargo')
        user.is_active = True if request.POST.get('active') == 'on' else False
        user.save()

        messages.success(request, 'Alterações salvas com sucesso!')
        return redirect('add-user')

    return render(request, 'pages/user-detail.html', {'user': user, 'empresas': empresas, 'cargos': cargos})
    