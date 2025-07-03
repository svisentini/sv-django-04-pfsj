from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST

from .forms import JoiaForm, ClienteForm
from .models import Joia, TipoJoia, Cliente

# Create your views here.
def index(request):
    return HttpResponse("Essa é a view index do APP polls")

#--------------------------------------------------------------------------------------------------
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

    return render(request, 'pfsj/listar_joias.html', {
        'joias': listaJoias,
        'tipos': listaTipos,
        'user_can_add':  request.user.has_perm('pfsj.add_joia'),
        'user_can_edit': request.user.has_perm('pfsj.change_joia'),
        'user_can_delete': request.user.has_perm('pfsj.delete_joia'),
    })

#--------------------------------------------------------------------------------------------------
@login_required
def cadastrar_joia(request):
    print(f"#### DEBUG INÍCIO CADASTRAR_JOIA: Request Method is {request.method} ####") 

    if request.method == 'POST':
        print("DEBUG: Método é POST. Prosseguindo com o formulário.") # Este print confirma que o método é POST
        form = JoiaForm(request.POST, request.FILES)

        if form.is_valid():
            print("DEBUG: Formulário é válido. Salvando joia.") # Este print se o formulário é válido
            joia = form.save()
            messages.success(request, f'Joia "{joia.codigo}" criada com sucesso!')
            return JsonResponse({
                'success': True,
                'message': f'Joia "{joia.codigo}" cadastrada com sucesso!',
                'new_joia_data': {
                    'id': joia.id,
                    'codigo': joia.codigo,
                    'descricao': joia.descricao,
                    'preco_venda': str(joia.preco_venda),
                    'quantidade': joia.quantidade,
                    'foto_url': joia.foto.url if joia.foto else '',
                    'tipo_id': joia.tipo.id,
                    'tipo_nome': joia.tipo.nome,
                    'ativo': joia.ativo,
                }
            })
        else:
            # ESTE BLOCO AGORA ESTÁ CORRETO:
            # Se o método É POST, mas o formulário NÃO É VÁLIDO (ex: código duplicado),
            # retorne os erros do formulário com status 400.
            print("DEBUG: Formulário NÃO é válido. Erros:", form.errors) # Este print mostra os erros
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        # Este bloco lida com requisições que NÃO são POST (ex: GET).
        # É onde o 405 é retornado, o que é o comportamento esperado para métodos não permitidos.
        print(f"DEBUG: Método NÃO é POST ({request.method}). Retornando 405.")
        return JsonResponse({'success': False, 'errors': {'__all__': 'Método não permitido. (view >> cadastrar_joia)'}}, status=405)

# O código NUNCA DEVE CHEGAR AQUI se a lógica acima estiver correta.
# Portanto, a linha final de `return JsonResponse` que estava causando o problema
# pode ser removida ou nunca será atingida se a lógica estiver certa.

#--------------------------------------------------------------------------------------------------
@login_required
def alterar_joia(request):
    print(f"#### DEBUG INÍCIO ALTERAR_JOIA: Request Method is {request.method} ####") 
    if request.method == 'POST':
        joia_id = request.POST.get('alterar_joia_id')
        if not joia_id:
            # Se não houver ID, retorna um erro JSON
            return JsonResponse({'success': False, 'errors': {'__all__': 'ID da joia não fornecido.'}}, status=400)

        try:
            joia_instance = Joia.objects.get(pk=joia_id)
        except Joia.DoesNotExist:
            return JsonResponse({'success': False, 'errors': {'__all__': 'Joia não encontrada.'}}, status=404)

        form = JoiaForm(request.POST, request.FILES, instance=joia_instance, for_update=True)

        if form.is_valid():
            joia = form.save()
            messages.success(request, f'Joia "{joia.codigo}" alterada com sucesso!')
            # Retorna um JSON de sucesso. O JavaScript fechará a modal e recarregará.
            return JsonResponse({
                'success': True,
                'message': f'Joia "{joia.codigo}" alterada com sucesso!',
                # Opcional: pode retornar os dados atualizados da joia se precisar
                # 'joia_data': {
                #     'id': joia.id,
                #     'codigo': joia.codigo,
                #     'descricao': joia.descricao,
                #     # ... outros campos
                # }
            })
        else:
            # Retorna um JSON com os erros do formulário.
            # form.errors já é um dicionário que pode ser serializado para JSON.
            # O JavaScript usará isso para exibir os erros na modal.
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    
    # Se a requisição não for POST, retorna um erro ou redireciona para a listagem
    return JsonResponse({'success': False, 'errors': {'__all__': 'Método não permitido.'}}, status=405)

#--------------------------------------------------------------------------------------------------
@login_required
def excluir_joia(request, id):
    joia = get_object_or_404(Joia, id=id)

    if request.method == "POST":
        joia.delete()
        messages.success(request, "Joia excluída com sucesso!")
        return redirect("listaJoias")

    messages.error(request, "Erro ao excluir a joia.")
    return redirect("listaJoias")

#==================================================================================================================================================
#==== Cliente
#==================================================================================================================================================


@login_required
def lista_clientes(request):
    # Opcional: Implementar filtros para nome, telefone, etc., se desejar
    filter_nome = request.GET.get('nome', '')
    filter_telefone = request.GET.get('telefone', '')

    clientes = Cliente.objects.all() # Busca todos os clientes por padrão

    if filter_nome:
        clientes = clientes.filter(nome__icontains=filter_nome)
    if filter_telefone:
        clientes = clientes.filter(telefone__icontains=filter_telefone)
    
    # Ordenar por nome para manter a lista organizada
    clientes = clientes.order_by('nome')

    # Instancie um formulário vazio para o modal de cadastro de novo cliente
    form_cadastro_cliente = ClienteForm()

    return render(request, 'pfsj/listar_clientes.html', {
        'clientes': clientes,
        'form_cadastro_cliente': form_cadastro_cliente, # Passa o formulário para o template
        'user_can_add':  request.user.has_perm('pfsj.add_cliente'), # Permissões
        'user_can_edit': request.user.has_perm('pfsj.change_cliente'),
        'user_can_delete': request.user.has_perm('pfsj.delete_cliente'),
    })


#--------------------------------------------------------------------------------------------------
@login_required
@permission_required('pfsj.add_cliente', raise_exception=True) # Requer permissão para adicionar cliente
@require_POST
def cadastrar_cliente(request):
    form = ClienteForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Cliente cadastrado com sucesso!')
        return JsonResponse({'success': True, 'message': 'Cliente cadastrado com sucesso!'})
    else:
        # Se o formulário não for válido, retorna os erros em formato JSON
        # form.errors contém um dicionário com os erros, por exemplo: {'nome': ['Este campo é obrigatório.']}
        return JsonResponse({'success': False, 'errors': form.errors}, status=400) # Status 400 para Bad Request

#--------------------------------------------------------------------------------------------------
@login_required
@permission_required('pfsj.change_cliente', raise_exception=True) # Requer permissão para alterar cliente
@require_POST
def alterar_cliente(request):
    cliente_id = request.POST.get('cliente_id')
    cliente = get_object_or_404(Cliente, pk=cliente_id) # Tenta buscar o cliente, ou retorna 404
    
    # Instancia o formulário com os dados da requisição e a instância do cliente
    form = ClienteForm(request.POST, instance=cliente)
    
    if form.is_valid():
        form.save()
        messages.success(request, 'Cliente alterado com sucesso!')
        return JsonResponse({'success': True, 'message': 'Cliente alterado com sucesso!'})
    else:
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)

#--------------------------------------------------------------------------------------------------
@login_required
@permission_required('pfsj.delete_cliente', raise_exception=True) # Requer permissão para excluir cliente
@require_POST
def excluir_cliente(request, id): # Recebe o ID do cliente da URL
    cliente = get_object_or_404(Cliente, pk=id)
    cliente.delete() # Exclui o cliente do banco de dados
    messages.success(request, 'Cliente excluído com sucesso!')
    return JsonResponse({'success': True, 'message': 'Cliente excluído com sucesso!'})


#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
