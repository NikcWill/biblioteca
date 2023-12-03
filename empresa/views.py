from django.shortcuts import render, HttpResponse,redirect
from.models import Empresas
from random import randint
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from accounts.models import CustomUser, Cargos
from django.contrib import messages
from django.db.models import Q
from accounts.models import CustomUser
from bibliotecaApp.models import Genero, Livro
from cliente.models import Cliente, Emprestimo
from django.db.models import Count


@login_required(redirect_field_name='login')
def empresa_detail(request, id):
  empresa = Empresas.objects.get(id=id)
  return render(request, 'pages/empresa_detail.html', {'empresa': empresa})

@login_required(redirect_field_name='login')
def add_empresa(request):
    if not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para adicionar uma empresa.', extra_tags='warning')
        return redirect('home')

    if request.method == 'POST':
        cod = randint(100, 10000)
        name = request.POST.get('name')
        cnpj = request.POST.get('cnpj')
        active = True
        created_at = datetime.now()

        gerente_cargo, _ = Cargos.objects.get_or_create(name='Gerente')
        operacional_cargo, _ = Cargos.objects.get_or_create(name='Operacional')

        if not gerente_cargo:
            gerente_cargo = Cargos.objects.create(name='Gerente')

        if not operacional_cargo:
            operacional_cargo = Cargos.objects.create(name='Operacional')

        new_empresa = Empresas.objects.create(
            cod=cod, name=name, cnpj=cnpj, active=active,
            created_at=created_at
        )

        # Realiza os cálculos das contagens para a nova empresa
        new_empresa.total_users = CustomUser.objects.filter(empresa_id=new_empresa.id).count()
        new_empresa.total_books = Livro.objects.filter(empresa_id=new_empresa.id).count()
        new_empresa.total_loans = Emprestimo.objects.filter(cliente__empresa_id=new_empresa.id, devolvido=False).count()
        new_empresa.total_clients = Cliente.objects.filter(empresa_id=new_empresa.id).count()

        # Salva as atualizações no banco de dados
        new_empresa.save()

        messages.success(request, 'Empresa Criada com sucesso.', extra_tags='success')

    # Atualiza os totais de todas as empresas existentes
    empresas = Empresas.objects.all()
    for empresa in empresas:
        empresa.total_users = CustomUser.objects.filter(empresa_id=empresa.id).count()
        empresa.total_books = Livro.objects.filter(empresa_id=empresa.id).count()
        empresa.total_loans = Emprestimo.objects.filter(cliente__empresa_id=empresa.id, devolvido=False).count()
        empresa.total_clients = Cliente.objects.filter(empresa_id=empresa.id).count()
        empresa.save()
    
    return render(request, 'pages/add-empresa.html', {'empresas': empresas})

@login_required(redirect_field_name='login')
def desativar_empresa(request, id):
    if not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para desativar uma empresa.', extra_tags='warning')
        return redirect('home')

    empresa = get_object_or_404(Empresas, id=id)

    emprestimos_ativos = Emprestimo.objects.filter(
        Q(cliente__empresa_id=empresa.id, devolvido=False) | Q(livro__empresa_id=empresa.id, devolvido=False)
    ).exists()

    if emprestimos_ativos:
        messages.error(request, 'Existem empréstimos associados a esta empresa. Não é possível desativá-la.', extra_tags='warning')
        return redirect('add-empresa')

    Cliente.objects.filter(empresa_id=empresa.id).update(active=False)
    Livro.objects.filter(empresa_id=empresa.id).update(in_stock=False)
    Genero.objects.filter(empresa_id=empresa.id).update(active=False)
    CustomUser.objects.filter(empresa_id=empresa.id).update(is_active=False)

    empresa.active = False
    empresa.save()

    messages.success(request, 'Empresa desativada com sucesso.', extra_tags='success')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER') + '?desativar_empresa=true')

@login_required(redirect_field_name='login')
def ativar_empresa(request, id):
    if not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para ativar uma empresa.', extra_tags='warning')
        return redirect('home')

    empresa = get_object_or_404(Empresas, id=id)

    Cliente.objects.filter(empresa_id=empresa.id).update(active=True)
    Livro.objects.filter(empresa_id=empresa.id).update(in_stock=True)
    Genero.objects.filter(empresa_id=empresa.id).update(active=True)
    CustomUser.objects.filter(empresa_id=empresa.id).update(is_active=True)

    empresa.active = True
    empresa.save()

    messages.success(request, 'Empresa ativada com sucesso.', extra_tags='success')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER') + '?ativar_empresa=true')