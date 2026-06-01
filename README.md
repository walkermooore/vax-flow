# VaxFlow 💉

> Sistema de backend robusto para gestão de imunização, integrando cidadãos, unidades de saúde e gestores em uma plataforma segura e escalável.

![Python](https://img.shields.io/badge/python-3.13+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?style=flat&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-316192.svg?style=flat&logo=postgresql&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success)

---

## 📑 Sumário

- [Funcionalidades](#-funcionalidades)
- [Arquitetura](#-arquitetura-do-sistema)
- [Perfis de Usuário](#-perfis-de-usuário)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Instalação](#-instalação)
- [Variáveis de Ambiente](#-variáveis-de-ambiente)
- [Exemplos de Uso](#-exemplos-de-uso)
- [Documentação da API](#-documentação-da-api)
- [Testes](#-testes)
- [Roadmap](#-roadmap)
- [Licença](#-licença)
- [Autores](#-autores)

---

## ✨ Funcionalidades

- **Gestão de Usuários:** Autocadastro, autenticação JWT e controle de acesso baseado em papéis (RBAC).
- **Agendamento Inteligente:** Reserva de horários para vacinação com validação de disponibilidade.
- **Controle de Estoque:** Gestão de lotes de vacinas com controle de validade e baixa automática.
- **Histórico Digital:** Carteira de vacinação digital acessível para o cidadão.
- **Gestão Operacional:** Cadastro de unidades de saúde, campanhas sazonais e agendas.
- **Relatórios & Auditoria:** Visões gerenciais de cobertura vacinal e rastreabilidade de ações.

## 🏗️ Arquitetura do Sistema

O sistema utiliza uma arquitetura multicamadas para garantir a separação de responsabilidades:

```mermaid
graph TD
    Client[Navegador/App] --> API[FastAPI Endpoints]
    API --> Auth[Middleware de Autenticação JWT]
    Auth --> Controllers[Controladores de Negócio]
    Controllers --> Schemas[Validação Pydantic]
    Controllers --> Models[Modelos SQLAlchemy]
    Models --> DB[(PostgreSQL)]
```

## 👥 Perfis de Usuário

### 👤 Cidadão
- Consultar carteira digital de vacinação.
- Agendar vacinação em unidades disponíveis.
- Consultar histórico de doses aplicadas.

### 🧑‍⚕️ Técnico (Saúde)
- Registrar aplicações de vacinas.
- Gerenciar estoque de lotes na unidade.
- Validar agendamentos.

### 👨‍💼 Gestor
- Criar e gerenciar campanhas de vacinação.
- Gerar relatórios de cobertura vacinal.
- Gerenciar unidades de saúde e usuários.

## 📁 Estrutura do Projeto

```text
.
├── alembic/              # Migrações do banco de dados
├── app/                  # Código-fonte principal
│   ├── api/              # Camada de transporte (Rotas e Controllers)
│   ├── auth/             # Segurança e Autenticação
│   ├── core/             # Configurações e Core do sistema
│   ├── db/               # Sessão e Conexão com Banco
│   ├── models/           # Entidades do Banco de Dados
│   ├── schema/           # Validação de dados (Pydantic)
│   └── templates/        # Interface HTML (Jinja2)
├── tests/                # Suíte de testes (Pytest)
├── pyproject.toml        # Dependências e Tasks
└── .env                  # Configurações de ambiente
```

## 🚀 Instalação

### Pré-requisitos

- Python 3.13+
- PostgreSQL 16+
- [uv](https://github.com/astral-sh/uv) (Gerenciador de pacotes)
- Docker (opcional)

### Passo a Passo

1. **Clonar o projeto**
   ```bash
   git clone https://github.com/leowalker/vaxflow.git
   cd vaxflow
   ```

2. **Configurar o ambiente**
   Crie um arquivo `.env` baseado no `.env_example`:
   ```bash
   cp .env_example .env
   ```

3. **Instalar dependências**
   ```bash
   uv sync
   ```

4. **Rodar as migrações**
   ```bash
   task up
   ```

5. **Executar o servidor**
   ```bash
   task run
   ```
   A API estará disponível em `http://localhost:7000`.

## 🔐 Variáveis de Ambiente

| Variável | Descrição | Exemplo |
| :--- | :--- | :--- |
| `DATABASE_URL` | URL de conexão com o banco | `postgresql://user:pass@localhost:5432/db` |
| `SECRET_KEY` | Chave para assinatura do JWT | `minha_chave_secreta_super_segura` |
| `DEBUG` | Ativa modo de desenvolvimento | `True` |
| `FIRST_SUPERUSER` | Email do admin inicial | `admin@healthnexus.com` |

## 📡 Exemplos de Uso

### Autenticação (Login)
> **Nota:** O login utiliza `application/x-www-form-urlencoded` para envio de credenciais.

```bash
curl -X POST "http://localhost:7000/login/access-token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin@example.com&password=password123"
```

### Criar Agendamento
```bash
curl -X POST "http://localhost:7000/agendamentos/" \
     -H "Authorization: Bearer <SEU_TOKEN>" \
     -H "Content-Type: application/json" \
     -d '{
           "vacina_id": "uuid-da-vacina",
           "unidade_id": "uuid-da-unidade",
           "data": "2026-06-01T10:00:00"
         }'
```

## 📚 Documentação da API

Uma vez iniciado o servidor, você pode acessar a documentação interativa e testar os endpoints diretamente pelo navegador:

- **Swagger UI:** [http://localhost:7000/docs](http://localhost:7000/docs)
- **Redoc:** [http://localhost:7000/redoc](http://localhost:7000/redoc)

![Swagger UI](docs/assets/tutorial.svg)

## 🧪 Testes

O projeto utiliza **Pytest** com foco em testes de integração e regras de negócio.
- **Unitários:** Validação de schemas e utilitários.
- **Integração:** Fluxos completos de agendamento e autenticação.

```bash
task test  # Executa a suíte completa
```

## 🗺️ Roadmap

- [ ] Integração com APIs de Mapas (Geolocalização).
- [ ] Geração de Certificado Nacional de Vacinação em PDF.
- [ ] Notificações via WhatsApp/Push.
- [ ] Aplicativo Mobile (Flutter).

## 📄 Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para obter mais informações.

## 👨‍💻 Autores

- **Léo Walker** - [GitHub](https://github.com/leowalker) | [LinkedIn](https://linkedin.com/in/leowalker)
- **[Nome do Colega]** - [GitHub](...) | [LinkedIn](...)
