from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST

from .forms import JoiaForm
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


def cadastrar_joia(request):
    if request.method == 'POST':
        form = JoiaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listaJoias')  # Ajuste para a página de listagem depois
    else:
        form = JoiaForm()

    return render(request, 'pfsj/cadastro_joia.html', {'form': form})

@require_POST
def excluir_joia(request, joia_id):
    joia = get_object_or_404(Joia, id=joia_id)
    joia.delete()
    return JsonResponse({'status':'success'})
