# Adega
## Sobre
A Adega é um sistema simples de Gerenciamento de Inventário.

A Adega foi especialmente desenvolvida para atender as necessidades de gestão de estoque da Secretaria de TI da Prefeitura de Vinhedo.

A iniciativa faz parte da primeira disciplina de [Projeto Integrador](https://apps.univesp.br/o-que-e-projeto-integrador/) da [Univesp](https://univesp.br/) no primeiro semestre de 2025.

## Quem
A Adega foi desenvolvida, no backend e front-end, por **Rodrigo Viana Rocha** e teve como gerentes de produto e design os demais colegas da **Univesp 2025, GRUPO-012, PJI110-SALA-004**:
- Ana Carolina Ferreira Alves Barcaro
- Andre Wilson Santanna Silva
- Carolina Ferreira Alves
- Daniela Almeida Vieira
- Jean Gustavo da Cunha Marinho
- Leonardo do Valle
- Rodrigo Viana Rocha
- Vanderlei Caetano de Souza
- Zairemylli Francislayne Carreira M Silva

## Características e Funcionalidades
- **Design responsível** para dispositivos móveis e desktops.
- O **tema** da Adega se adequa imediatamente ao tema do sistema operacional do usuário (dark/light mode).
- Gestão de **Usuários** e **Superusuários**.
- Gestão de **Endereços** com preenchimento automático a partir de um CEP válido.
- Gestão de **Pessoas Físicas e Jurídicas** (com validação automática de CPF e CNPJ).
- Gestão de **Categorias** de Itens e **Itens Individuais**.
- Módulo de **Transações** para registrar atividades de:
    - Compra
    - Venda
    - Doação
    - Empréstimo
    - Retorno
    - Transferência
    - Descarte

- **Relatórios de Estoque**
    - por Categoria
    - por itens

- **Ajuda** com exemplos de funcionalidade.

- **Tabelas dinâmicas** com busca avançada para todos os itens tabelados, com ordenação por colunas.

- **Perfomance comprovada e testada**: teste com entidades com mais de 1 milhão de registros, sem causar problemas às funcionalidades ou banco de dados do sistema.

## Tecnologias utilizadas
A Adega foi desenvolvida utilizando o framework web fullstack de `Python`, o `Django`.

Devido a essa escolha - e suas soluções prontas para as camadas de modelo, visualização e template - nos parece que não faz sentido usar algo como React para o frontend. Em vez disso, estamos usando `Bootstrap` e algumas outras ferramentas para construir os componentes voltados para o usuário.

Lista de linguagens, frameworks e bibliotecas utilizadas:
- **Python**
- **Django**
    - **django-crispy-forms**: aprimorar visualmente os formulários
    - **django-select2**: campos dropdown com buscas
- **Bootstrap**: web framework
- **jQuery**: dependência de diversas bibliotecas javascript utilizads
    - **jQuery Mask**: para criar máscaras nos campos de formulários (ex: CPF e CNPJ)
- **DataTables**: tabelas dinâmicas
- **Faker** (dependência de desenvolvimento): usado para criar milhões de registros para testes

## Configuração do ambiente de desenvolvimento

### 1. Instalando o pipx
O `Poetry` é o gerenciador de pacotes escolhido para o projeto.
O `Poetry` recomenda sua instalação através do `pipx`.
Por favor, siga os [passos](https://github.com/pypa/pipx?tab=readme-ov-file#install-pipx) apropriados
de acordo com o seu Sistema Operacional.

### 2. Instalando o Poetry
```bash
pipx install poetry
```

### 3. Instalando o projeto Adega
Na raiz do projeto `adega\`, instale as dependências do projeto:
```bash
poetry install
```

Crie a tabela de cache para o `select2`:
```bash
poetry run python manage.py createcachetable select2_cache_table
```

Execute as migrações do projeto:
```bash
poetry run python manage.py makemigrations
poetry run python manage.py migrate --run-syncdb
```

### 4. Criando um superusuário
Crie um `superuser` do `Django` para o projeto. Através deste usuário você poderá criar:
```bash
poetry run python manage.py createsuperuser
```

### 5. Rodando o servidor interno do Django
Tudo pronto! Agora você pode iniciar o servidor web leve do Django para desenvolvimento:
```bash
poetry run python manage.py runserver
```

### 6. Abrindo o projeto no navegador
O projeto estará disponível em [http://127.0.0.1:8000](http://127.0.0.1:8000) e poderá ser acessado através do seu navegador:
```bash
google-chrome http://127.0.0.1:8000
```

## Configuração do ambiente de produção

### Detalhes do ambiente de desenvolvimento
Na seção anterior, foi demonstrado como você pode configurar e rodar o projeto Adega em um ambiente de desenvolvimento: um conjunto de configurações propício para criar novas funcionalidades e resolver eventuais bugs.

O arquivo de configuração `adega/settings.py` está preparado justamente para o cenário de desenvolvimento:
- A `SECRET_KEY` é insegura e está publicada nesse Github.
- O banco de dados padrão é `sqlite3`.
- O modo de debug está ligado (`DEBUG = True`).
- O servidor utilizado é o simples `runserver` do Django.


### Detalhes do ambiente de desenvolvimento
No ambiente de produção devemos ter:
- Uma Django `SECRET_KEY` segura e não publicada. Ela somente existirá em um secret manager e será injetada no ambiente de produção via variável de ambiente.
- O banco de dados proposto é o `PostgreSQL`, mas você pode usar outro banco de dados, desde que o Django tenha suporte.
- O modo de debug deve estar desligado (`DEBUG = False`).
- O servidor utilizado deve ser um servidor WSGI adequado para produção, como o `gunicorn`.

### 1. Ajustando o settings.py para produção
Para o ambiente de produção sugerimos substituir o arquivo padrão de configurações, `adega/settings.py` por `adega/settings_prod.py`:
```bash
cp adega/settings_prod.py adega/settings.py
```
Obs: Lembre-se de ajustar a lista `ALLOWED_HOSTS` para o domínio do seu servidor dentro do `settings.py`!!!

### 2. Instalando libs locais para conexão com PostgreSQL
Para o Django conseguir conectar com o banco é necessário que o sistema operacional tenha a biblioteca PostgreSQL instalada. No Ubuntu isso pode ser feito com o seguinte comando:
```bash
sudo apt-get install libpq-dev
```

### 3. Containerizando o projeto
- Na raiz do projeto, `adega\`, existe uma proposta de containerização  com o `Docker`. O arquivo `compose.yaml` contém as instruções para subir os containers necessários para rodar o projeto em produção.
- O arquivo `Dockerfile` contém as instruções para criar a imagem do projeto específica para atender as dependências do projeto em si.
Você deve ter o `Docker` instalado e poderá subir os container prontos com o comando:
- Se você quiser testar localmente esses containers, o primeiro passo é ter as variáveis de ambiente simuladas. Para isso:
```bash
cp .env.example .env
```
- Agora pode subir todo o ambiente de produção com o comando:
```bash
sudo docker compose up -d
```
