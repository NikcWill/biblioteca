from django.shortcuts import render, HttpResponse, redirect
from bibliotecaApp.models import Livro
from .models import Cliente, Emprestimo
from random import randint
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from django.http import JsonResponse
from uuid import uuid4
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.contrib import messages

def get_clientes_based_on_permission(user):
    if user.is_superuser:
        return Cliente.objects.all()
    elif user.cargo.name == 'Gerente':
        return Cliente.objects.filter(empresa_id=user.empresa.id)
    else:
        return Cliente.objects.filter(user_id=user.id)
    
  
def get_clientes_based_active(user):
    if user.is_superuser:
        return Cliente.objects.filter(active=True)
    elif user.cargo.name == 'Gerente':
        return Cliente.objects.filter(empresa_id=user.empresa.id, active=True)
    else:
        return Cliente.objects.filter(user_id=user.id, active=True)


def get_livros_based_on_permission(user):
    if user.is_superuser:
        return Livro.objects.filter(in_stock=True)
    elif user.cargo.name == 'Gerente':
        return Livro.objects.filter(empresa_id=user.empresa.id, in_stock=True)
    else:
        return Livro.objects.filter(user_id=user.id, in_stock=True)


def get_livros_base_cliente(user, cliente):
    emprestimos_cliente = Emprestimo.objects.filter(cliente_id=cliente.id).values_list('livro_id', flat=True)

    if user.is_superuser:
        return Livro.objects.filter(in_stock=True, id__in=emprestimos_cliente)
    elif user.cargo.name == 'Gerente':
        return Livro.objects.filter(empresa_id=user.empresa.id, in_stock=True, id__in=emprestimos_cliente)
    else:
        return Livro.objects.filter(user_id=user.id, in_stock=True, id__in=emprestimos_cliente)

@login_required(redirect_field_name='login')
def cliente_detail(request, id):
    cliente = Cliente.objects.get(id=id)
    emprestimos = Emprestimo.objects.filter(cliente_id=id, devolvido=False)
    
    livros_emprestados = []
    data_prev_devolucao = None  

    if emprestimos.exists():  
        for emprestimo in emprestimos:
            livros_emprestados.append({
                'livro': emprestimo.livro,
                'cod_emprestimo': emprestimo.id,
                'data_prev_devolucao': emprestimo.data_prev_devolucao,
                'dias_para_devolver' : emprestimo.dias_para_devolver, 
            })

            data_prev_devolucao = emprestimo.data_prev_devolucao  
    else:
         livros_emprestados = []
     

    return render(request, 'pages/cliente_detail.html', {
        'cliente': cliente,
        'livros_emprestados': livros_emprestados,
        'data_prev_devolucao': data_prev_devolucao,
    })

@login_required(redirect_field_name='login')
def historico_cliente(request, id):
    cliente = Cliente.objects.get(id=id)
    emprestimos = Emprestimo.objects.filter(cliente_id=id, devolvido=True)
    
    livros_emprestados = []
    data_devolucao = None
    data_prev_devolucao = None
    saldo_de_dias_devolvidos = None 

    if emprestimos:
        for emprestimo in emprestimos:
            livros_emprestados.append({
                'livro': emprestimo.livro,
                'cod_emprestimo': emprestimo.id,
                'data_devolucao': emprestimo.data_devolucao,
                'data_prev_devolucao': emprestimo.data_prev_devolucao,
                'saldo_de_dias_devolvidos': emprestimo.saldo_de_dias_devolvidos
            })
            data_devolucao = emprestimo.data_devolucao
            data_prev_devolucao = emprestimo.data_prev_devolucao
            saldo_de_dias_devolvidos = emprestimo.saldo_de_dias_devolvidos

    return render(request, 'pages/historico-cliente.html', {
        'cliente': cliente,
        'livros_emprestados': livros_emprestados,
        'data_devolucao': data_devolucao,
        'data_prev_devolucao': data_prev_devolucao,
        'saldo_de_dias_devolvidos': saldo_de_dias_devolvidos  
    })

@login_required(redirect_field_name='login')
def clientes(request):
    clientes = get_clientes_based_active(request.user)
    return render(request, 'pages/clientes.html', {'clientes': clientes})


@login_required(redirect_field_name='login')
def add_cliente(request):
    if request.method == 'POST':
        cod = randint(100, 10000) 
        name = request.POST.get('name')
        cpf = request.POST.get('cpf')
        email = request.POST.get('email')
        active = True
        created_at = datetime.now()
        qtd_livros = 0

        Cliente.objects.create(
            user_id=request.user.id, empresa_id=request.user.empresa.id,
            cod=cod, name=name, cpf=cpf, email=email, active=active,
            created_at=created_at, qtd_livros=qtd_livros
        )
        messages.success(request, 'Cliente cadastrado com sucesso.', extra_tags='success')
        return redirect('add-cliente')
    else:
        clientes = get_clientes_based_on_permission(request.user)
        return render(request, 'pages/add-cliente.html', {'clientes': clientes})

@login_required(redirect_field_name='login')
def add_emprestimo(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        livros_selecionados = request.POST.getlist('livros_emprestimo[]')

        data_emprestimo = datetime.now().strftime('%Y-%m-%d') 
        data_prev_devolucao_str = request.POST.get('data_prev_devolucao')
        data_prev_devolucao = datetime.strptime(data_prev_devolucao_str, '%Y-%m-%d')
        data_devolucao = request.POST.get('data_devolucao')


        for livro_id in livros_selecionados:
            livro = Livro.objects.get(id=livro_id)
            if livro.in_stock and livro.emprestado < livro.qtd and not Emprestimo.objects.filter(cliente_id=cliente_id, livro_id=livro_id, data_devolucao__isnull=True).exists():
                cod_emprestimo = str(uuid4())

                Emprestimo.objects.create(
                    user_id=request.user.id,
                    empresa_id=request.user.empresa.id,
                    cod=cod_emprestimo,
                    cliente_id=cliente_id,
                    livro_id=livro_id,
                    data_emprestimo=data_emprestimo,
                    data_prev_devolucao=data_prev_devolucao,
                    data_devolucao=data_devolucao,
                    devolvido=False,
                    saldo_de_dias_devolvidos=0,
                    dias_para_devolver=data_calculate(data_prev_devolucao, data_emprestimo)

                )

                quantidade_emprestada_livro = Emprestimo.objects.filter(livro_id=livro_id, data_devolucao__isnull=True).count()
                livro.emprestado = quantidade_emprestada_livro
                livro.save()

        quantidade_emprestada_cliente = Emprestimo.objects.filter(cliente_id=cliente_id, data_devolucao__isnull=True).count()
        cliente = Cliente.objects.get(id=cliente_id)
        cliente.qtd_livros = quantidade_emprestada_cliente
        cliente.save()

        clientes = get_clientes_based_on_permission(request.user)
        livros = get_livros_based_on_permission(request.user)
        messages.success(
            request,
            f'O livro "{livro.name}" foi emprestado para o cliente "{cliente.name}"com sucesso.',
            extra_tags='success'
        )
        return render(request, 'pages/add-emprestimo.html', {'clientes': clientes, 'livros': livros})
    else:
        clientes = get_clientes_based_on_permission(request.user)
        livros = get_livros_based_on_permission(request.user)
        return render(request, 'pages/add-emprestimo.html', {'clientes': clientes, 'livros': livros})

@login_required(redirect_field_name='login')
def devolver_livro(request, emprestimo_id):
    emprestimo = get_object_or_404(Emprestimo, id=emprestimo_id)
    cliente = emprestimo.cliente

    if cliente.qtd_livros > 0:
        emprestimo.data_devolucao = datetime.now()
        emprestimo.devolvido = True
        emprestimo.saldo_de_dias_devolvidos = data_calculate(emprestimo.data_prev_devolucao.strftime('%Y-%m-%d'), datetime.now().strftime('%Y-%m-%d'))
        emprestimo.save()

        livro_devolvido = emprestimo.livro
        livro_devolvido.emprestado -= 1
        livro_devolvido.save()

        cliente.qtd_livros -= 1
        cliente.save()  

    redirect_url = request.META.get('HTTP_REFERER')
    messages.success(
            request,
            f'O livro "{livro_devolvido.name}" foi emprestado para o cliente "{cliente.name}"com sucesso.',
            extra_tags='success'
        )
    return HttpResponseRedirect(redirect_url or '/') 

@login_required(redirect_field_name='login')
def selecionar_cliente(request):
    q = request.GET.get('q')  

    user = request.user

    clientes = get_clientes_based_on_permission(user)

    cliente = get_object_or_404(clientes, id=q)

    livros_emprestados_cliente = Emprestimo.objects.filter(
        cliente_id=cliente.id, devolvido=False
    ).values_list('livro_id', flat=True)

    livros_nao_emprestados = Livro.objects.filter(
        in_stock=True, empresa_id=cliente.empresa_id
    ).exclude(
        Q(id__in=livros_emprestados_cliente) | Q(in_stock=False)
    )

    return render(request, 'pages/add-emprestimo.html', {
        'cliente': cliente,
        'livros_nao_emprestados': livros_nao_emprestados,
        'clientes': clientes,
    })


@login_required(redirect_field_name='login')
def emprestados_livros(request):
    user = request.user
    clientes = get_clientes_based_on_permission(user)
    
    livros_emprestados = Livro.objects.filter(
        id__in=Emprestimo.objects.filter(
            Q(cliente_id__in=[cliente.id for cliente in clientes]) & Q(devolvido=False)
        ).values_list('livro_id', flat=True)
    ).distinct()

    emprestimos_info = []
    for livro in livros_emprestados:
        emprestimos_livro = Emprestimo.objects.filter(livro=livro, devolvido=False)
        for emprestimo in emprestimos_livro:
            emprestimos_info.append({
                'livro': livro,
                'emprestimo': emprestimo,
                'cliente': emprestimo.cliente,
                'data_prev_devolucao': emprestimo.data_prev_devolucao,
                'dias_para_devolver' : emprestimo.dias_para_devolver, 
            })

    return render(request, 'pages/emprestados_livros.html', {
        'emprestimos_info': emprestimos_info,
    })


def data_calculate(data_1, data_2):
    if isinstance(data_1, str):
        data_1 = datetime.strptime(data_1, '%Y-%m-%d')
    if isinstance(data_2, str):
        data_2 = datetime.strptime(data_2, '%Y-%m-%d')

    diferenca = data_1 - data_2

    return diferenca.days

@login_required(redirect_field_name='login')
def deletar_emprestimo(request, emprestimo_id):
    if not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para deletar um empréstimo.', extra_tags='warning')
        return redirect('historico-cliente')

    emprestimo = get_object_or_404(Emprestimo, id=emprestimo_id)
    
    cliente = emprestimo.cliente
    livro = emprestimo.livro
    
    cliente.qtd_livros += 1
    cliente.save()

    livro.emprestado += 1
    livro.save()

    emprestimo.delete()
    
    messages.success(
        request,
        f'O livro "{livro.name}" foi deletado dos registros com sucesso.',
        extra_tags='success'
    )
    return HttpResponseRedirect(request.META.get('HTTP_REFERER') + '?emprestimo_deletado=true')

@login_required(redirect_field_name='login')
def desativar_cliente(request, id):
    
    cliente = get_object_or_404(Cliente, id=id)

    emprestimos_ativos = Emprestimo.objects.filter(
        cliente_id=cliente.id, devolvido=False
    ).exists()

    if emprestimos_ativos:
        messages.error(request, 'Existem empréstimos associados a este cliente. Não é possível desativá-lo.', extra_tags='warning')
        return redirect('add-cliente')

    cliente.active = False
    cliente.save()

    messages.success(request, 'Cliente desativado com sucesso.', extra_tags='success')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER') + '?desativar_cliente=true')
    
@login_required(redirect_field_name='login')
def ativar_cliente(request, id):
    
    cliente = get_object_or_404(Cliente, id=id)
    
    cliente.active = True
    cliente.save()

    messages.success(request, 'Cliente ativado com sucesso.', extra_tags='success')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER') + '?ativar_cliente=true')