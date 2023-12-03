from django.shortcuts import render, HttpResponse,redirect
from.models import Empresas
from random import randint
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect


@login_required(redirect_field_name='login')
def empresa_detail(request, id):
  empresa = Empresas.objects.get(id=id)
  return render(request, 'pages/empresa_detail.html', {'empresa': empresa})

@login_required(redirect_field_name='login')
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
    empresas = Empresas.objects.all()
    return render(request, 'pages/add-empresa.html', {'empresas': empresas})
  
def desativar_empresa(request, id):
    empresa = get_object_or_404(Empresas, id=id)
    empresa.active = False  
    empresa.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER') + '?desativar_empresa=true')

def ativar_empresa(request, id):
    empresa = get_object_or_404(Empresas, id=id)
    empresa.active = True  
    empresa.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER') + '?ativar_empresa=true')