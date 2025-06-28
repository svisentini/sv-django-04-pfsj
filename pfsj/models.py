from django.db import models
from django.utils import timezone
import datetime

# Create your models here.

class TipoJoia(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome


class Joia(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    descricao = models.TextField()
    preco_compra = models.DecimalField(max_digits=10, decimal_places=2)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.PositiveIntegerField()
    foto = models.ImageField(upload_to='joias/', blank=True, null=True)
    tipo = models.ForeignKey(TipoJoia, on_delete=models.CASCADE)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.codigo} - {self.descricao}"
    

class Cliente(models.Model):
    nome            = models.CharField      ( max_length=100,                        verbose_name="Nome Completo" )
    telefone        = models.CharField      ( max_length=20,  blank=True, null=True, verbose_name="Telefone"      )
    endereco        = models.CharField      ( max_length=255, blank=True, null=True, verbose_name="Endereço"      )
    observacao      = models.TextField      (                 blank=True, null=True, verbose_name="Observação"    )
    data_cadastro   = models.DateTimeField  ( auto_now_add=True                                                   ) # Registra a data e hora da criação automaticamente
    ativo           = models.BooleanField   ( default=True,                          verbose_name="Ativo"         ) # Flag para ativar/desativar

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes" # Nome no plural para o Django Admin
        ordering = ['nome'] # Ordena os clientes pelo nome por padrão

    def __str__(self):
        return self.nome # Representação em string do objeto Cliente