from django import forms
from .models import Joia, TipoJoia # Certifique-se de importar o TipoJoia também

class JoiaForm(forms.ModelForm):
    class Meta:
        model = Joia
        # Inclua todos os campos que você está editando no modal.
        # Não inclua 'codigo' se ele estiver 'disabled' e você não quer que seja editável após a criação.
        # Se 'codigo' for apenas para exibição, ele não precisa estar no form.
        fields = ['descricao', 'preco_compra', 'preco_venda', 'quantidade', 'foto', 'tipo', 'ativo']

        # Opcional: widgets personalizados para inputs específicos
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
            # Outros widgets se precisar personalizar o HTML gerado pelo form
        }

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