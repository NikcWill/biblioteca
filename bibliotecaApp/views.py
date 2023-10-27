from django.shortcuts import render, HttpResponse, redirect
from.models import Livro
from random import randint
from datetime import datetime
 

def index(request):

  #return HttpResponse('Estou no Django')
  #from Product select *

  livros = Livro.objects.all()
  return render(request, 'pages/index.html', {'livro':livros})


def livro_detail(request, id):
  livro = Livro.objects.get(id=id)
  return render(request, 'pages/livro_detail.html', {'livro': livro})

def delete_livro(request, id):
  livro = Livro.objects.get(id=id)
  livro.delete()
  return redirect('home')

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
    created_at = datetime.now()
    

    Livro.objects.create(
      cod=cod, name=name, genery=genery, pg=pg, picture=picture,
      author=author, qtd=qtd, name_sacado=name_sacado,
      created_at=created_at
    )
    return redirect('home')

  else:
    # genero = Genero.objects.all()
    return render(request, 'pages/add-livro.html')
