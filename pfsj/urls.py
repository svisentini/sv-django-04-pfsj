from django.urls import path
from . import views
from .views import cadastrar_joia

urlpatterns = [
    path("lista", views.lista_joias, name="listaJoias"),
    path("cadastrarjoia/", cadastrar_joia, name="cadastrarJoias"),
    path('joias/excluir/<int:id>/', views.excluir_joia, name='excluir_joia'),

]
