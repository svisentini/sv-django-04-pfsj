from django.shortcuts import render
from django.http import HttpResponse

from .models import Joia, TipoJoia

# Create your views here.
def index(request):
    return HttpResponse("Essa é a view index do APP polls")

def lista_joias(request):
    filter_codigo = request.GET.get('codigo', '')
    filter_descricao = request.GET.get('descricao', '')
    filter_tipo = request.GET.get('tipo', '')

    listaJoias = Joia.objects.filter(ativo=True)
    listaTipos = TipoJoia.objects.all()

    if filter_codigo:
        listaJoias = listaJoias.filter(codigo__icontains=filter_codigo)
    if filter_descricao:
        listaJoias = listaJoias.filter(descricao__icontains=filter_descricao)
    if filter_tipo:
        listaJoias = listaJoias.filter(tipo_id=filter_tipo)

    return render(request, 'pfsj/listar_produtos.html', {
        'joias': listaJoias,
        'tipos': listaTipos
    })

