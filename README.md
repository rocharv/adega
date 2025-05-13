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

### 2. Instale o Poetry
```bash
pipx install poetry
```
### 3. Instalação do projeto
- Na raiz do projeto `adega\`, instale as dependências do projeto:
```bash
poetry install
```

- Crie a tabela de cache para o `select2`
```bash
poetry run python manage.py createcachetable select2_cache_table
```

- Execute as migrações do projeto:
```bash
poetry run python manage.py makemigrations
poetry run python manage.py migrate --run-syncdb
```

- Crie um `superuser` do `Django` para o projeto. Através deste usuário você poderá criar:
```bash
poetry run python manage.py createsuperuser
```

- Tudo pronto! Agora você pode iniciar o servidor web leve do Django para desenvolvimento:
```bash
poetry run python manage.py runserver
```