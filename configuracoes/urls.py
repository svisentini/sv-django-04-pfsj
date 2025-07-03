"""
URL configuration for configuracoes project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from pfsj import views


urlpatterns = [
    # == URLs de Joias
    path("pfsj/cadastrarjoia/",            views.cadastrar_joia,   name="cadastrarJoias"   ),
    path("pfsj/alterarjoia/",              views.alterar_joia,     name="alterarJoias"     ),
    path("pfsj/lista",                     views.lista_joias,      name="listaJoias"       ),
    path('pfsj/joias/excluir/<int:id>/',   views.excluir_joia,     name='excluir_joia'     ),

    # == URLs de Cliente
    path("pfsj/clientes/",                 views.lista_clientes,   name="listaClientes"    ),
    path("pfsj/clientes/cadastrar/",       views.cadastrar_cliente,name="cadastrarClientes"),
    path("pfsj/clientes/alterar/",         views.alterar_cliente,  name="alterarClientes"  ),
    path("pfsj/clientes/excluir/<int:id>/",views.excluir_cliente,  name="excluir_cliente"  ),

    # == URLs de Admin, Login e Logout
    path('admin/',  admin.site.urls),
    path('login/',  LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

