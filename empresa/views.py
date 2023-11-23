from django.shortcuts import render, HttpResponse,redirect
from.models import Empresas
from random import randint
from datetime import datetime

def empresa_detail(request, id):
  empresa = Empresas.objects.get(id=id)
  return render(request, 'pages/empresa_detail.html', {'empresa': empresa})

def add_empresa(request, ):
  if request.method == 'POST':

    cod = randint(100, 10000)
    name = request.POST.get('name')
    cnpj = request.POST.get('cnpj')
    active = True
    created_at = datetime.now()
    
    Empresas.objects.create(
      cod=cod, name=name, cnpj=cnpj, active=active,
      created_at=created_at
    )
    return redirect('home')

  else:
    return render(request, 'pages/add-empresa.html')
