
# Estrutura do Diretório

---
Enim fugiat amet incididunt nostrud incididunt. Dolore et pariatur est in incididunt in aliqua pariatur quis quis aliquip officia eiusmod ipsum. Pariatur velit sint incididunt aliquip est fugiat ullamco sint ex qui tempor cillum reprehenderit.

Ullamco magna in dolore nisi fugiat eiusmod magna culpa excepteur adipisicing qui consectetur enim labore. Duis incididunt cupidatat velit sunt occaecat elit anim mollit minim occaecat nisi dolor. Nostrud aliquip tempor nisi velit velit aliqua in. Velit eu elit non minim. Reprehenderit mollit et amet nulla elit id in est qui consequat eu magna esse sit. Laboris proident duis consequat sint tempor ex aliqua aute reprehenderit. Occaecat fugiat culpa eiusmod nisi occaecat anim officia laboris.

Officia voluptate amet amet dolore fugiat nulla tempor ad minim reprehenderit sint id eiusmod. Lorem incididunt commodo exercitation pariatur do id esse nostrud. Proident qui deserunt culpa nulla fugiat nulla culpa excepteur amet fugiat excepteur laborum. Sit occaecat elit laboris deserunt eiusmod ullamco magna minim dolore culpa sunt reprehenderit non nulla. Eiusmod voluptate proident laboris dolor fugiat mollit cupidatat.

---

## Arvore de diretorio

    backend
    ├── alembic
    │   └── versions
    ├── app
    │   ├── api
    │   │   └── v1
    │   │       └── endpoints
    │   ├── auth
    │   ├── core
    │   ├── database
    │   ├── db
    │   ├── models
    │   ├── schema
    │   ├── static
    │   │   ├── assets
    │   │   ├── css
    │   │   ├── img
    │   │   ├── js
    │   │   └── scss
    │   ├── templates
    │   ├── uploads
    │   └── util
    ├── docs
    │   ├── app
    │   │   ├── api
    │   │   │   ├── endpoints
    │   │   │   └── integration
    │   │   ├── auth
    │   │   ├── core
    │   │   ├── database
    │   │   ├── db
    │   │   ├── models
    │   │   ├── schemas
    │   │   ├── static
    │   │   │   ├── css
    │   │   │   ├── img
    │   │   │   ├── js
    │   │   │   └── scss
    │   │   ├── templates
    │   │   ├── uploads
    │   │   └── utils
    │   ├── assets
    │   └── stylesheets
    ├── htmlcov
    └── tests
        └── file_test

- **app**: Nível da aplicação, encapsula os módulos da aplicação `./backend/app/`
- **api**: Contém todos os endpoints do aplicativo `./backend/app/api/`
- **auth**:Se necessário, contém as regras de autenticação do aplicação, padrão de autorização baseado em OAuth 2.0 Permite que aplicativos como Web App, Mobile e Desktop obtenham acesso limitado às informações do usuário`./backend/app/auth/`.
- **core**: Contém todas as variáveis de ambiente usadas na aplicação `./backend/app/core/`, obtendo arquivos `.env` como fonte em `./`
- **database**: Se houver necessidade de pré-preencher os dados, eles devem ficar neste nível`./backend/app/database/`.
- **db**: Configuraçoes de conexão e construção do banco de dados `./backend/app/db/`.
- **models**: Deve conter todos os modelos do banco de dados. Modifique ou adicione modelos SQLAlchemy em `./backend/app/models/`
- **schema**: Responsável por validar a estrutura de dados antes de permitir a entrada em um endpoint.
- **static**: Somente se houver necessidade de elementos estáticos no projeto.
- **templates**: Se necessário, deve conter os templates do projeto.
- **uploads**: Se necessário, diretorio para salvar arquivos. sura `uri` pode ser alterada em `.env` contido em `./`.
- **util**: Módulo que contém métodos que podem ou não ser reutilizados em diferentes projetos.
- **docs**: Se existir, deve conter a documentação da aplicaçao `./backend/docs/`
- **tests**: O cenário ideal. Escreva seus testes. `./back-end/tests/`
- **.env**: Todas as variáveis de ambiente podem ser encontradas no diretório `./backand/`(o arquivo `.env`)
- **Dependências**: Todas as dependências podem ser encontradas no diretório `./backend` (o arquivo `pyproject.toml` e `requiriments.txt`)
