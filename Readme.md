## 📦 Configuração do Ambiente
Este documento descreve o passo a passo para configurar o ambiente de desenvolvimento do projeto localmente.

## ✅ Pré-requisitos
Antes de começar, certifique-se de ter instalado:

- Python (versão conforme definida no projeto)
- Git
- Docker e Docker Compose

## 🧰 Instalação das ferramentas

### 1️⃣ Instalar o Poetry
O Poetry é utilizado para gerenciamento de dependências e ambiente virtual.

#### Linux / macOS
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

#### Windows (PowerShell)
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

Após a instalação, verifique:
```bash
poetry --version
```

### 2️⃣ Instalar o Just
O Just é utilizado para automatizar comandos do projeto.

#### Linux / macOS (com Cargo)
```bash
cargo install just
```

#### Windows (com Chocolatey)
```powershell
choco install just
```

Verifique a instalação:
```bash
just --version
```

## 📥 Instalação das dependências do projeto

Com o repositório clonado e dentro da pasta do projeto, execute:
```bash
poetry install
```

Esse comando irá:
- Criar o ambiente virtual
- Instalar todas as dependências definidas no `pyproject.toml`

## ⚙️ Configuração do ambiente

1. **Crie o arquivo `.env`**
   - O dev que te deu acesso ao repo também fornecerá esse arquivo
   - Coloque na raiz do projeto

2. **Construa e inicie os containers Docker**:
```bash
just build
just start
```

3. **Execute as migrações do Alembic**:
```bash
just migrate
```

Isso criará/atualizará o schema do banco de dados.

## 🚀 Comandos úteis

Aqui estão os principais comandos disponíveis no projeto:

| Comando | Descrição |
|---------|-----------|
| `just build` | Constrói as imagens Docker |
| `just start` | Inicia os containers em background |
| `just stop` | Para os containers |
| `just reload` | Para e reinicia os containers |
| `just shell` | Acessa o shell do container da API |
| `just migrate` | Executa as migrações do Alembic |
| `just makemigrations "descricao"` | Cria uma nova migração automática |
| `just test` | Executa os testes com pytest |
| `just test -v` | Executa os testes com mais detalhes |
| `just exec fast-api <comando>` | Executa um comando qualquer no container |

## 📝 Observações

- Caso tenha problemas com versões de Python, verifique o arquivo `pyproject.toml`
- Recomenda-se usar sempre os comandos via `just` para manter o ambiente consistente
- Para ver todos os comandos disponíveis, abra o arquivo `Justfile` na raiz do projeto
- O projeto usa **Alembic** para controle de migrações do banco de dados