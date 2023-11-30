from django.shortcuts import render, HttpResponse, redirect
from bibliotecaApp.models import Livro
from .models import Cliente, Emprestimo
from random import randint
from datetime import datetime
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(redirect_field_name='login')
def add_cliente(request ):
  if request.method == 'POST':

    cod = randint(100, 10000)
    name = request.POST.get('name')
    cpf = request.POST.get('cpf')
    email = request.POST.get('email')
    active = True
    created_at = datetime.now()

    Cliente.objects.create(
      user_id=request.user.id, empresa_id=request.user.empresa.id,
      cod=cod, name=name, cpf=cpf, email=email, active=active,
      created_at=created_at
      )
    return redirect('home')
  else:  # Para requisições GET, renderize o formulário de adição de cliente
        return render(request, 'pages/add-cliente.html')

@login_required(redirect_field_name='login')
def add_emprestimo(request ):
  if request.method == 'POST':

    cod = randint(100, 10000)
    cliente = request.POST.get('cliente')
    livro = request.POST.get('livro')
    data_emprestimo = datetime.now()
    data_prev_devolucao_str = request.POST.get('data_prev_devolucao')
    data_prev_devolucao = datetime.strptime(data_prev_devolucao_str, '%d/%m/%Y').strftime('%Y-%m-%d')
    data_devolucao = request.POST.get('data_devolucao')
    
    Emprestimo.objects.create(
      user_id=request.user.id, empresa_id=request.user.empresa.id,
      cod=cod, cliente_id=cliente, livro_id=livro, data_emprestimo=data_emprestimo,
      data_prev_devolucao=data_prev_devolucao, data_devolucao=data_devolucao
      )
    return redirect('home')
  else:
    
    if request.user.is_superuser:
        clientes = Cliente.objects.all()
    elif request.user.cargo.name == 'Gerente':
        clientes = Cliente.objects.filter(empresa_id=request.user.empresa.id)
    else:
        clientes = Cliente.objects.filter(user_id=request.user.id)

    if request.user.is_superuser:
        livros = Livro.objects.filter(in_stock=True)
    elif request.user.cargo.name == 'Gerente':
        livros = Livro.objects.filter(empresa_id=request.user.empresa.id, in_stock=True)
    else:
        livros = Livro.objects.filter(user_id=request.user.id, in_stock=True)

    return render(request, 'pages/add-emprestimo.html', {'clientes': clientes, 'livros': livros})

  