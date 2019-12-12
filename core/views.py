from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout


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

    evento = Evento.objects.filter(usuario = usuario) #eventos do usuário logado.
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