# sv-django-04-pfsj
Paula Fernandes Semijoias


1) Criar ambiente virtual e ativar
Linux:
		python3 -m venv .venv         >> Cria um Ambiente Virtual
		source .venv/bin/activate     >> Entra no Ambiente Virtual

2) Instalar o Django (dentro do ambiente virtual >> criado e ATIVADO no passo 1)
	pip install django

Para saber que esta dentro do ambiente virtual, verificar no inicio da linha de comando (.venv)

	
3) Criar um projeto (Projeto é um conjunto de app >> app seria cada funcionalidade)
	django-admin startproject configuracoes .
	Cria um projeto chamado mysite dentro do diretorio atual (indicado pelo ".")

4) Rodar projeto
	python manage.py runserver

5) Criar um APP -- Aplicação(deve estar com o Ambiente Virtual ativo)
    python manage.py startapp polls

<<==== Criação do ambiente ===>

6) Settings.py >> Arquivo com configurações do Projeto.
   LANGUAGE_CODE = 'pt-br'
   TIME_ZONE = 'America/Sao_Paulo'

7) python manage.py migrate
   Para criar as tabelas no Banco de dados

8) Criar os modelos em models.py
   Adicionar a aplicação no projeto
   settings.py >> Installed apps >> pfsj.apps.PfsjConfig
   python manage.py makemigrations pfsj
      Cria or arquivos de migração
      Precisa incluir no settings pois apenas os aplicativos que estao la é que sao considerados.

9) python manage.py sqlmigrate pfsj 0001
   Apenas EXIBE o SQL da migration selecionada.
   python manage.py migrate >> Para rodar a migration no banco.

https://docs.djangoproject.com/pt-br/5.1/intro/tutorial02/#creating-an-admin-user

10) Criar um usuario para acessar a area de administração
    python manage.py createsuperuser
    admin   svisentini@gmail.com    pfsjadm123    (usuario e-mail pwd ...)

11) Para que o objeto "Joia" apareca na pagina de adminstração, precisamos informar
    admin.py >> from .models import Joia >> admin.site.register(Question)

https://docs.djangoproject.com/pt-br/5.1/intro/tutorial03/#writing-more-views

<<==== Publicar o projeto no Render ===>

Preparação do Projeto para produção:
- settings.py >> defina DEBUG=False (True é usado na etapa de desenvolvimento apenas)
- Configure ALLOWED_HOSTS para incluir o domínio que você usará (por exemplo, ['*'] para permitir qualquer domínio temporariamente).
- Configure o STATIC_URL e STATIC_ROOT para servir arquivos estáticos.
- Crie um arquivo com as dependencias do Projeto
    pip freeze > requirements.txt
- Um arquivo Procfile (para definir o comando de execução do servidor).
    Exemplo de Procfile:
    web: gunicorn seu_projeto.wsgi



































