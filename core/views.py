from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from datetime import datetime,timedelta
from django.http.response import Http404,JsonResponse


# Create your views here.

def eventos(request,titulo_evento):
    evento = Evento.objects.get(titulo=titulo_evento)
    return HttpResponse(evento.descricao)

# def index(request):
#     return redirect('/agenda/')

@login_required(login_url='/login/')
def lista_eventos(request):
    #evento = Evento.objects.get(id=1)
    usuario = request.user

    data_atual = datetime.now() - timedelta(hours=1) # aparecer evento menos que 1 hora
    evento = Evento.objects.filter(usuario=usuario,
                                   data_evento__gt=data_atual) #eventos do usuário logado.

    #evento = Evento.objects.all()
    dados = {'eventos': evento}
    return render(request,'agenda.html', dados)

def login_user(request):
    return render(request,'login.html')

def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        #autenticacao
        usuario = authenticate(username=username,password=password)
        if usuario is not None:
            login(request,usuario)
            return redirect('/')
        else:
            messages.error(request,'Usuário e senha inválido.')
    return redirect('/')


def logout_user(request):
    user = logout(request)
    return redirect('/')

@login_required(login_url='/login/')
def evento(request):
    id_evento = request.GET.get('id')
    dados = {}
    if id_evento:
        dados['evento'] = Evento.objects.get(id=id_evento)
    return render(request,'evento.html',dados)


@login_required(login_url='/login/')
def submit_evento(request):
    if request.POST:

        titulo = request.POST.get('titulo')
        data_evento =request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        local = request.POST.get('local')
        usuario = request.user

        if data_evento == "":
            messages.error(request, 'Data de evento não definida.')
        else:
            id_evento = request.POST.get('id_evento')
            if id_evento:
                evento - Evento.objects.get(id=id_evento)
                if evento.usuario == usuario:
                    Evento.objects.filter(id=id_evento).update(
                                            titulo=titulo,
                                            data_evento= data_evento,
                                            descricao = descricao,
                                            local=local
                                            )
                else:
                    messages.error(request, 'Usuário não tem permissão desta operação.')
            else:
                Evento.objects.create(titulo=titulo,
                                      data_evento= data_evento,
                                      descricao = descricao,
                                      local = local,
                                      usuario = usuario)
    return redirect('/')

@login_required(login_url='/login/')
def delete_evento(request,id_evento):
    usuario = request.user
    try:
        evento = Evento.objects.get(id=id_evento)
    except Exception:
        raise Http404()

    if usuario == evento.usuario:
        evento.delete()
    else:
        raise Http404()
    return redirect('/')

#@login_required(login_url='/login/')
def json_lista_evento(request):
    usuario = request.user
    evento = Evento.objects.filter(usuario=usuario).values('id','titulo')
    return JsonResponse(list(evento),safe=False)

def json_lista_evento_id(request,id_usuario):
    usuario = User.objects.get(id=id_usuario)
    evento = Evento.objects.filter(usuario=usuario).values('id','titulo')
    return JsonResponse(list(evento),safe=False)

