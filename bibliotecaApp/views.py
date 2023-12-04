from django.shortcuts import render, HttpResponse, redirect
from.models import Livro, Genero
from cliente.models import Emprestimo
from random import randint
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def is_manager_or_superuser(user):
    return user.is_superuser or (user.cargo.name == 'Gerente')

@login_required(redirect_field_name='login')
def delete_livro(request, id):
    if not is_manager_or_superuser(request.user):
        messages.error(request, 'Você não tem permissão para excluir este livro.',extra_tags='warning')
        return redirect('livro-detail', id=livro.id) 

    livro = Livro.objects.get(id=id)
    if livro.emprestado <= 0:
        livro.delete()
        messages.success(request, 'Livro deletado com sucesso.', extra_tags='success')
        return redirect('home')
    else:
        messages.error(request, 'Não é possível deletar livros emprestados.', extra_tags='warning')
    return redirect('livro-detail', id=livro.id)

@login_required(redirect_field_name='login')
def index(request):
    if request.user.is_superuser:
        livros = Livro.objects.filter(in_stock=True)
    elif request.user.cargo.name == 'Gerente':
        livros = Livro.objects.filter(empresa_id=request.user.empresa.id, in_stock=True)
    else:
        livros = Livro.objects.filter(user_id=request.user.id, in_stock=True)

    return render(request, 'pages/index.html', {'livros': livros})

@login_required(redirect_field_name='login')
def search_livros(request):
  q = request.GET.get('q')
  if request.user.is_superuser:
        livros = Livro.objects.filter(name__icontains=q,in_stock=True)
  elif request.user.cargo.name == 'Gerente':
      livros = Livro.objects.filter(name__icontains=q,empresa_id=request.user.empresa.id, in_stock=True)
  else:
      livros = Livro.objects.filter(name__icontains=q,user_id=request.user.id, in_stock=True)

  return render(request, 'pages/index.html', {'livros': livros})

@login_required(redirect_field_name='login')
def search_livros_emprestados(request):
  q = request.GET.get('q')
  if request.user.is_superuser:
        livros = Livro.objects.filter(name__icontains=q,emprestado__gt=0,in_stock=True)
  elif request.user.cargo.name == 'Gerente':
      livros = Livro.objects.filter(name__icontains=q,emprestado__gt=0,empresa_id=request.user.empresa.id, in_stock=True)
  else:
      livros = Livro.objects.filter(name__icontains=q,emprestado__gt=0,user_id=request.user.id, in_stock=True)

  return render(request, 'pages/livros-emprestados.html', {'livros':livros})

@login_required(redirect_field_name='login')
def livros_emprestados(request):
    if request.user.is_superuser:
        livros = Livro.objects.filter(emprestado__gt=0,in_stock=True)
    elif request.user.cargo.name == 'Gerente':
        livros = Livro.objects.filter(emprestado__gt=0,empresa_id=request.user.empresa.id, in_stock=True)
    else:
        livros = Livro.objects.filter(emprestado__gt=0,user_id=request.user.id, in_stock=True)

    return render(request, 'pages/livros-emprestados.html', {'livros': livros})

  
@login_required(redirect_field_name='login')    
def livro_detail(request, id):
  livro = Livro.objects.get(id=id)
  return render(request, 'pages/livro_detail.html', {'livro': livro})


@login_required(redirect_field_name='login')
def add_livro(request, ):
  if request.method == 'POST':

    cod = randint(100, 10000)
    name = request.POST.get('name')
    genery = request.POST.get('genery')
    pg = request.POST.get('pg')
    picture = request.FILES.get('picture')
    author = request.POST.get('author')
    qtd = request.POST.get('qtd')
    in_stock = True
    created_at = datetime.now()
    emprestado = 0
    

    Livro.objects.create(
      user_id=request.user.id, empresa_id=request.user.empresa.id,
      cod=cod, name=name, genery_id=genery, pg=pg, picture=picture,
      author=author, qtd=qtd,
      created_at=created_at, in_stock=in_stock, emprestado=emprestado
    )
    messages.success(request, 'Livro adicionado com sucesso.', extra_tags='success')
    return redirect('add-livro')

  else:
    if request.user.is_superuser:
        livros = Livro.objects.all()
    elif request.user.cargo.name == 'Gerente':
        livros = Livro.objects.filter(empresa_id=request.user.empresa.id)
    else:
        livros = Livro.objects.filter(user_id=request.user.id)
    
    if request.user.is_superuser:
        genero = Genero.objects.all()
    elif request.user.cargo.name == 'Gerente':
        genero = Genero.objects.filter(empresa_id=request.user.empresa.id)
    else:
        genero= Genero.objects.filter(user_id=request.user.id)
    

    return render(request, 'pages/add-livro.html', {'generos': genero,'livros': livros})

@login_required(redirect_field_name='login')
def add_genero(request):
    if request.method == 'POST':
        cod = randint(100, 10000)
        name = request.POST.get('name')
        active = True

        existente_genero = Genero.objects.filter(name=name).first()
        if existente_genero:
            messages.error(request, 'Não é possível criar este gênero pois há livros emprestados associados a ele.', extra_tags='warning')
            return redirect('add-genero')
        else:
            new_genero = Genero.objects.create(
                user_id=request.user.id, empresa_id=request.user.empresa.id,
                name=name, cod=cod, active=active
            )
            messages.success(request, 'Gênero criado com sucesso.', extra_tags='success')
            return redirect('add-genero')

    else:
        if request.user.is_superuser:
            if not request.user.empresa:
                messages.error(request, 'Não existe empresa cadastrada! Para adicionar é necessário adicionar uma!.', extra_tags='warning')
                return redirect('add-empresa')
            else:
                genero = Genero.objects.filter(active=True)
        elif request.user.cargo.name == 'Gerente':
            genero = Genero.objects.filter(empresa_id=request.user.empresa.id, active=True)
        else:
            genero = Genero.objects.filter(user_id=request.user.id, active=True)

        return render(request, 'pages/add-genero.html', {'generos': genero})

@login_required(redirect_field_name='login')
def delete_genero(request, id):
    genero = Genero.objects.get(id=id)

    livros_emprestados = Livro.objects.filter(genery=genero, emprestado__gt=0)
    
    if livros_emprestados.exists():
        messages.error(request, 'Não é possível excluir este gênero pois há livros emprestados associados a ele.', extra_tags='warning')
    else:
        genero.delete()
        messages.success(request, 'Gênero excluído com sucesso.', extra_tags='success')

    return redirect('add-genero')

@login_required(redirect_field_name='login')
def desativar_livro(request, id):
    livro = Livro.objects.get(id=id)
    
    emprestimos_ativos = Emprestimo.objects.filter(livro_id=id, devolvido=False).exists()
    
    if emprestimos_ativos:
        messages.error(request, 'Não é possível desativar o livro. Existem empréstimos pendentes associados a ele.', extra_tags='warning')
    else:
        livro.in_stock = False
        livro.save()
        messages.success(request, 'Livro desativado.', extra_tags='success')
    
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(redirect_field_name='login')
def ativar_livro(request, id):
    livro = Livro.objects.get(id=id)
    livro.in_stock = True
    livro.save()

    messages.success(request, 'Livro ativado.', extra_tags='success')
    
    return redirect(request.META.get('HTTP_REFERER'))
    