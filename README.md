
O **VaxFlow** é um sistema de backend robusto para gestão de imunização, integrando cidadãos, unidades de saúde e gestores em uma plataforma segura e escalável.

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

## 🔐 Variáveis de Ambiente
| Variável | Descrição | Exemplo |
| :--- | :--- | :--- |
| `DATABASE_URL` | URL de conexão com o banco | `postgresql://user:pass@localhost:5432/db` |
| `SECRET_KEY` | Chave para assinatura do JWT | `minha_chave_secreta_super_segura` |
| `DEBUG` | Ativa modo de desenvolvimento | `True` |
| `FIRST_SUPERUSER` | Email do admin inicial | `admin@healthnexus.com` |

## 📡 Exemplos de Requisições
### Autenticação (Login)
```bash
curl -X POST "http://localhost:7000/api/v1/login" \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com", "password": "password123"}'
```

### Criar Agendamento
```bash
curl -X POST "http://localhost:7000/api/v1/agendamentos" \
     -H "Authorization: Bearer <SEU_TOKEN>" \
     -H "Content-Type: application/json" \
     -d '{"vacina_id": "uuid", "unidade_id": "uuid", "data": "2026-06-01"}'
```

## 🧪 Cobertura de Testes
O projeto utiliza **Pytest** com foco em testes de integração e regras de negócio.
- **Unitários:** Validação de schemas e utilitários.
- **Integração:** Fluxos completos de agendamento e autenticação.
```bash
task test  # Executa a suíte completa
```

**VaxFlow** is a robust backend system for immunization management, connecting citizens, health units, and managers in a secure and scalable platform.

## ✨ Features
- **User Management:** Self-registration, JWT authentication, and Role-Based Access Control (RBAC).
- **Smart Scheduling:** Vaccination slot reservation with availability validation.
- **Inventory Control:** Vaccine batch management with expiration control and automatic deduction.
- **Digital Records:** Accessible digital vaccination card for citizens.
- **Operational Management:** Registration of health units, seasonal campaigns, and schedules.
- **Reports & Auditing:** Managerial views of vaccination coverage and action traceability.

## 🏗️ System Architecture
The system utilizes a multi-layer architecture to ensure separation of concerns:

```mermaid
graph TD
    Client[Browser/App] --> API[FastAPI Endpoints]
    API --> Auth[JWT Auth Middleware]
    Auth --> Controllers[Business Controllers]
    Controllers --> Schemas[Pydantic Validation]
    Controllers --> Models[SQLAlchemy Models]
    Models --> DB[(PostgreSQL)]
```

## 📁 Project Structure
```text
.
├── alembic/              # Database migrations
├── app/                  # Main source code
│   ├── api/              # Transport layer (Routes and Controllers)
│   ├── auth/             # Security and Authentication
│   ├── core/             # Global configurations and System core
│   ├── db/               # Session and Database Connection
│   ├── models/           # Database Entities
│   ├── schema/           # Data validation (Pydantic)
│   └── templates/        # HTML Interface (Jinja2)
├── tests/                # Test suite (Pytest)
├── pyproject.toml        # Dependencies and Tasks
└── .env                  # Environment configurations
```

## 🔐 Environment Variables
| Variable | Description | Example |
| :--- | :--- | :--- |
| `DATABASE_URL` | DB connection URL | `postgresql://user:pass@localhost:5432/db` |
| `SECRET_KEY` | Key for JWT signing | `my_super_secure_secret_key` |
| `DEBUG` | Enables development mode | `True` |
| `FIRST_SUPERUSER`| Initial admin email | `admin@healthnexus.com` |

## 📡 Request Examples
### Authentication (Login)
```bash
curl -X POST "http://localhost:7000/api/v1/login" \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com", "password": "password123"}'
```

### Create Scheduling
```bash
curl -X POST "http://localhost:7000/api/v1/agendamentos" \
     -H "Authorization: Bearer <YOUR_TOKEN>" \
     -H "Content-Type: application/json" \
     -d '{"vacina_id": "uuid", "unidade_id": "uuid", "data": "2026-06-01"}'
```

## 🧪 Test Coverage
The project uses **Pytest** with a focus on integration tests and business rules.
- **Unit:** Schema and utility validation.
- **Integration:** Complete scheduling and authentication flows.
```bash
task test  # Runs the full suite
```

## 🗺️ Roadmap
- [ ] Integration with Maps APIs (Geolocation).
- [ ] National Vaccination Certificate generation in PDF.
- [ ] WhatsApp/Push notifications.
- [ ] Mobile App (Flutter).
