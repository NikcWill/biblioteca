from django.shortcuts import render, HttpResponse, redirect
from.models import Livro, Genero
from random import randint
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def is_manager_or_superuser(user):
    return user.is_superuser or (user.cargo.name == 'Gerente')

def delete_livro(request, id):
    if not is_manager_or_superuser(request.user):
        messages.error(request, 'Você não tem permissão para excluir este livro.')
        return redirect('home')  

    livro = Livro.objects.get(id=id)
    if livro.emprestado <= 0:
        livro.delete()
    return redirect('home')

def index(request):
    if request.user.is_superuser:
        livros = Livro.objects.filter(in_stock=True)
    elif request.user.cargo.name == 'Gerente':
        livros = Livro.objects.filter(empresa_id=request.user.empresa.id, in_stock=True)
    else:
        livros = Livro.objects.filter(user_id=request.user.id, in_stock=True)

    return render(request, 'pages/index.html', {'livros': livros})

def search_livros(request):
  q = request.GET.get('q')
  if request.user.is_superuser:
        livros = Livro.objects.filter(name__icontains=q,in_stock=True)
  elif request.user.cargo.name == 'Gerente':
      livros = Livro.objects.filter(name__icontains=q,empresa_id=request.user.empresa.id, in_stock=True)
  else:
      livros = Livro.objects.filter(name__icontains=q,user_id=request.user.id, in_stock=True)

  return render(request, 'pages/index.html', {'livros': livros})
  
def search_livros_emprestados(request):
  q = request.GET.get('q')
  if request.user.is_superuser:
        livros = Livro.objects.filter(name__icontains=q,emprestado__gt=0,in_stock=True)
  elif request.user.cargo.name == 'Gerente':
      livros = Livro.objects.filter(name__icontains=q,emprestado__gt=0,empresa_id=request.user.empresa.id, in_stock=True)
  else:
      livros = Livro.objects.filter(name__icontains=q,emprestado__gt=0,user_id=request.user.id, in_stock=True)

  return render(request, 'pages/livros-emprestados.html', {'livros':livros})

def livros_emprestados(request):
    if request.user.is_superuser:
        livros = Livro.objects.filter(emprestado__gt=0,in_stock=True)
    elif request.user.cargo.name == 'Gerente':
        livros = Livro.objects.filter(emprestado__gt=0,empresa_id=request.user.empresa.id, in_stock=True)
    else:
        livros = Livro.objects.filter(emprestado__gt=0,user_id=request.user.id, in_stock=True)

    return render(request, 'pages/livros-emprestados.html', {'livros': livros})


@login_required(redirect_field_name='login')
def emprestar_livro(request, id):
  livro = Livro.objects.get(id=id)
  if livro.emprestado < livro.qtd:
    livro.emprestado += 1
    livro.save()
    
  referer = request.META.get('HTTP_REFERER')  
  if 'livro-detail' in referer:
      return redirect('livro-detail', id=id)
  elif 'livros-emprestados' in referer:
      return redirect('livros-emprestados')

@login_required(redirect_field_name='login')
def devolver_livro(request, id):
  livro = Livro.objects.get(id=id)
  if livro.emprestado > 0:
    livro.emprestado -= 1
    livro.save()
    
  referer = request.META.get('HTTP_REFERER')
  if 'livro-detail' in referer:
      return redirect('livro-detail', id=id)
  elif 'livros-emprestados' in referer:
      return redirect('livros-emprestados')
  
     
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
    name_sacado = request.POST.get('name_sacado')
    in_stock = True
    created_at = datetime.now()
    emprestado = 0
    

    Livro.objects.create(
      user_id=request.user.id, empresa_id=request.user.empresa.id,
      cod=cod, name=name, genery_id=genery, pg=pg, picture=picture,
      author=author, qtd=qtd, name_sacado=name_sacado,
      created_at=created_at, in_stock=in_stock, emprestado=emprestado
    )
    return redirect('home')

  else:
    genero = Genero.objects.all()
    return render(request, 'pages/add-livro.html', {'generos': genero})
