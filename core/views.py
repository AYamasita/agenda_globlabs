from django.shortcuts import render, HttpResponse, redirect

# Create your views here.
from core.models import Evento


def eventos(request,titulo_evento):
    evento = Evento.objects.get(titulo=titulo_evento)
    return HttpResponse(evento.descricao)

# def index(request):
#     return redirect('/agenda/')


def listaeventos(request):
    #evento = Evento.objects.get(id=1)
    # evento = Evento.objects.filter(usuario = usuario) // eventos do usuário logado.
    evento = Evento.objects.all()
    dados = {'eventos': evento}
    return render(request,'agenda.html', dados)