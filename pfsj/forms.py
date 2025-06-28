from django import forms
from .models import Joia, TipoJoia, Cliente # Certifique-se de importar o TipoJoia também

class JoiaForm(forms.ModelForm):
    class Meta:
        model = Joia
        # Inclua todos os campos que você está editando no modal.
        # Não inclua 'codigo' se ele estiver 'disabled' e você não quer que seja editável após a criação.
        # Se 'codigo' for apenas para exibição, ele não precisa estar no form.
        fields = ['codigo', 'descricao', 'preco_compra', 'preco_venda', 'quantidade', 'foto', 'tipo', 'ativo']

        # Opcional: widgets personalizados para inputs específicos
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
            # Outros widgets se precisar personalizar o HTML gerado pelo form
            'preco_compra': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'preco_venda': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'quantidade': forms.NumberInput(attrs={'min': '0'}),
        }

    def __init__(self, *args, **kwargs):
        # Pega um argumento personalizado 'for_update' se ele for passado
        self.for_update = kwargs.pop('for_update', False)
        super().__init__(*args, **kwargs)

        # Se o formulário é para ALTERAÇÃO, remova o campo 'codigo'
        if self.for_update and 'codigo' in self.fields:
            self.fields['codigo'].required = False # Opcional: torna não obrigatório
            del self.fields['codigo'] # Remove o campo do formulário

    # Você pode adicionar validações customizadas aqui, se necessário.
    # Exemplo: garantir que o preço de venda seja maior que o preço de compra
    def clean(self):
        cleaned_data = super().clean()
        preco_compra = cleaned_data.get('preco_compra')
        preco_venda = cleaned_data.get('preco_venda')

        if preco_compra and preco_venda and preco_venda < preco_compra:
            self.add_error('preco_venda', 'O preço de venda não pode ser menor que o preço de compra.')
        return cleaned_data

    # Se 'codigo' é disabled no HTML e você o incluiu no 'fields',
    # e ele é 'unique=True', talvez seja necessário uma lógica para tratá-lo
    # como um campo somente leitura que não causa erro de validação de unicidade
    # se não for alterado. ModelForms geralmente lidam bem com 'instance'.


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        # Liste todos os campos que você quer que apareçam no formulário
        fields = ['nome', 'telefone', 'endereco', 'observacao', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo do cliente'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: (XX) XXXX-XXXX'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rua, número, bairro, cidade'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Informações adicionais sobre o cliente'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}), # Bootstrap checkbox
        }

    # Opcional: Se você quisesse tratar campos de forma diferente para atualização,
    # você usaria o __init__ como fizemos no JoiaForm.
    # Exemplo: Se 'nome' fosse unique=True e você quisesse desabilitá-lo na edição
    # def __init__(self, *args, **kwargs):
    #     self.for_update = kwargs.pop('for_update', False)
    #     super().__init__(*args, **kwargs)
    #     if self.for_update and 'nome' in self.fields:
    #         self.fields['nome'].widget.attrs['readonly'] = True # Torna o campo somente leitura na edição