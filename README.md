# API Pizzaria

API REST para gerenciamento de contas de clientes e pedidos de uma pizzaria. O projeto usa FastAPI, SQLAlchemy, SQLite e autenticação com tokens JWT.

## Funcionalidades

- Criar conta de usuário e armazenar senha com hash bcrypt.
- Autenticar por JSON ou formulário OAuth2 e emitir token JWT.
- Criar pedidos e adicionar ou remover itens.
- Consultar pedidos próprios; administradores podem listar todos os pedidos.
- Cancelar e finalizar pedidos, com verificação de proprietário ou administrador.
- Documentação interativa gerada pelo FastAPI em `/docs`.

## Tecnologias

- Python
- FastAPI e Uvicorn
- SQLAlchemy e SQLite
- Alembic para migrações
- JWT (`python-jose`) e hash bcrypt (`passlib`)

## Pré-requisitos

- Python 3.10 ou superior
- `pip`

## Instalação e execução

Clone o repositório, crie e ative um ambiente virtual:

```bash
git clone https://github.com/SEU_USUARIO/api-pizzaria.git
cd api-pizzaria
python -m venv .venv
```

No Windows (PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
```

No macOS/Linux:

```bash
source .venv/bin/activate
```

Instale as dependências e prepare as variáveis de ambiente:

```bash
pip install -r requirements.txt
```

Copie `.env.example` para `.env` e defina uma chave secreta forte. Nunca compartilhe nem envie o `.env` ao GitHub.

```env
SECRET_KEY=uma-chave-longa-aleatoria
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Inicie a API:

```bash
uvicorn main:app --reload
```

A API ficará disponível em `http://127.0.0.1:8000`. Consulte `/docs` para explorar e executar as rotas e `/redoc` para a documentação alternativa.

## Banco de dados

Por padrão, a aplicação conecta ao SQLite em `banco.db`, criado no diretório do projeto. O arquivo do banco é local e está excluído do Git. As migrações do Alembic ficam em `alembic/versions` e podem ser aplicadas com:

```bash
alembic upgrade head
```

## Rotas

Todas as rotas abaixo usam o prefixo indicado. As rotas de pedidos exigem `Authorization: Bearer <access_token>`.

### Autenticação (`/auth`)

| Método | Caminho | Descrição |
| --- | --- | --- |
| GET | `/auth/` | Rota inicial de autenticação |
| POST | `/auth/criar_conta` | Cria uma conta; recebe `nome`, `email`, `senha` e, opcionalmente, `ativo` e `admin` |
| POST | `/auth/login` | Autentica via JSON (`email` e `senha`) e retorna access e refresh tokens |
| POST | `/auth/login-form` | Autentica via formulário OAuth2 e retorna access token |
| GET | `/auth/refresh` | Emite novo access token usando um token válido |

### Pedidos (`/pedidos`)

| Método | Caminho | Descrição |
| --- | --- | --- |
| GET | `/pedidos/` | Rota inicial de pedidos |
| POST | `/pedidos/pedido` | Cria um pedido para o `id_usuario` informado |
| GET | `/pedidos/pedido/{id_pedido}` | Consulta um pedido próprio ou, como administrador, qualquer pedido |
| POST | `/pedidos/pedido/adicionar-item/{id_pedido}` | Adiciona item com `quantidade`, `sabor`, `tamanho` e `preco_unitario` |
| POST | `/pedidos/pedido/remover-item/{id_item_pedido}` | Remove um item do pedido |
| POST | `/pedidos/pedido/cancelar/{id_pedido}` | Cancela pedido próprio ou de administrador |
| POST | `/pedidos/pedido/finalizar/{id_pedido}` | Finaliza pedido próprio ou de administrador |
| GET | `/pedidos/listar/pedidos-usuario` | Lista pedidos do usuário autenticado |
| GET | `/pedidos/listar` | Lista todos os pedidos; somente administrador |




- Revise permissões de cadastro e configuração de usuários administradores antes de disponibilizar a API publicamente.
