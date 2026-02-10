# Apache Airflow - Aula Prática (Lighthouse)

Este repositório contém o material prático para a aula de **Apache Airflow** do programa **Lighthouse** da **Indicium AI**.

O Lighthouse é o programa de formação da Indicium voltado para quem deseja iniciar uma carreira em dados, IA ou negócios. Este projeto serve como base educacional para demonstrar **boas práticas**, padrões de arquitetura e funcionalidades essenciais do Airflow rodando em Docker.

---

## Sumário

1. [Sobre o Projeto](#sobre-o-projeto)
2. [Estrutura do Repositório](#estrutura-do-repositório)
3. [Configuração Inicial e Instalação](#configuração-inicial-e-instalação)
    - [Pré-requisitos](#pré-requisitos)
    - [Configurando o AIRFLOW_UID (Linux/Mac)](#configurando-o-airflow_uid-linuxmac)
    - [Configurando Variáveis de Ambiente](#configurando-variáveis-de-ambiente)
4. [Executando o Projeto](#executando-o-projeto)
    - [Rodando com Logs (Foreground)](#rodando-com-logs-foreground)
    - [Rodando em Background (Sem travar terminal)](#rodando-em-background-sem-travar-terminal)
    - [Rodando sem Rebuildar (Mais rápido)](#rodando-sem-rebuildar-mais-rápido)
    - [Parando e Limpando Tudo](#parando-e-limpando-tudo)
5. [Resolução de Problemas (Troubleshooting)](#resolução-de-problemas-troubleshooting)
6. [Visão Geral das DAGs](#visão-geral-das-dags)

---

## Sobre o Projeto

O objetivo é fornecer exemplos claros de como gerenciar variáveis, criar pipelines ETL, utilizar a TaskFlow API moderna e interagir com banco de dados e containers.

Neste projeto, utilizamos containers com nomes fixos para facilitar o gerenciamento:

- `airflow_webserver`: Interface Web
- `airflow_scheduler`: Agendador de tarefas
- `airflow_postgres`: Banco de dados de metadados
- `airflow_init`: Serviço de inicialização (roda e para rapidamente)

## Estrutura do Repositório

```text
.
├── dags/                        # Diretório principal das DAGs (fluxos de trabalho)
│   ├── 1_dag_variables.py       # Variáveis via UI do Airflow
│   ├── 2_dag_variables_utils.py # Modularização com Utils
│   ├── 3_dag_variables_env.py   # Variáveis de Ambiente (.env)
│   ├── 4_dag_variables_code.py  # Variáveis via Código (Config)
│   ├── 5_dag_api_pipeline.py    # Pipeline ETL Real (API -> CSV)
│   ├── 6_dag_docker_check.py    # DockerOperator (Container Efêmero)
│   ├── 7_dag_postgres_conn.py   # Conexão com Postgres (Operator)
│   ├── 8_dag_postgres_hook.py   # Conexão com Postgres (Hook/Python)
│   ├── 9_dag_dynamic_tasks.py   # Geração Dinâmica de Tasks
│   └── utils/                   # Funções auxiliares reutilizáveis
├── outputs/                     # Diretório mapeado para saída de arquivos gerados
├── logs/                        # Logs de execução do Airflow
├── plugins/                     # Plugins customizados do Airflow
├── .env.example                 # Exemplo de arquivo de configuração
├── .env                         # Variáveis de ambiente (criado por você)
├── docker compose.yaml          # Orquestração dos containers
├── Dockerfile                   # Imagem customizada do Airflow
└── requirements.txt             # Dependências Python extras
```

---

## Configuração Inicial e Instalação

### Pré-requisitos

- **Docker Engine** e **Docker Compose** instalados.
  - [Guia de Instalação do Docker Compose](https://docs.docker.com/compose/install/)

### Configurando o AIRFLOW_UID (Linux/Mac)

O Airflow roda dentro do container com um usuário não-root. No Linux, se os arquivos criados pelo Airflow (logs, dags) tiverem permissões diferentes do seu usuário local, você não conseguirá editá-los (ou o Airflow não conseguirá acessá-los).

Para corrigir isso, precisamos dizer ao container para rodar com **o mesmo ID do seu usuário local**.

1. Descubra o seu ID de usuário rodando no terminal:

   ```bash
   id -u
   ```

   *Geralmente retorna `1000`.*

### Configurando Variáveis de Ambiente

1. Crie um arquivo `.env` na raiz do projeto (use o `.env.example` como base):

   ```bash
   cp .env.example .env
   ```

2. Abra o arquivo `.env` e ajuste o `AIRFLOW_UID` com o valor obtido no passo anterior (ex: 50000 ou 1000):

   ```env
   AIRFLOW_UID=1000
   ```

   *Se não configurar, o padrão será 50000.*

### (Opcional) Ambiente Virtual Python Local

Para ter autocompletion na sua IDE (VSCode, PyCharm) e rodar scripts locais, recomenda-se criar um ambiente virtual:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Acessando a Interface do Airflow

Após rodar o comando `docker compose up` e aguardar a inicialização dos containers, abra seu navegador e acesse:

- **URL:** [http://localhost:8080](http://localhost:8080)
- **Usuário:** `admin`
- **Senha:** `admin`

---

## Executando o Projeto

### Rodando com Logs (Foreground)

Ideal para a primeira execução ou debugging, para ver tudo o que está acontecendo.

```bash
docker compose up --build
```

- Use `Ctrl+C` para parar (isso vai parar os containers).*

### Rodando em Background (Sem travar terminal)

Ideal para o dia a dia. Libera o terminal logo após subir os serviços.

```bash
docker compose up -d --build
```

### Rodando sem Rebuildar (Mais rápido)

Se você não alterou o `Dockerfile` nem o `requirements.txt`, não precisa da flag `--build`.

```bash
docker compose up -d
```

### Parando e Limpando Tudo

Para parar os containers e remover a rede criada:

```bash
docker compose down
```

**⚠️ Reset Total (Apagar Banco de Dados):**
Se quiser começar do zero e apagar todas as configurações e histórico de DAGs (excluindo o volume do Postgres):

```bash
docker compose down -v
```

*Isso vai deletar o volume `postgres-db-volume` onde os dados do Airflow ficam salvos.*

---

## Configurando a Conexão Postgres (Necessário para DAGs 7 e 8)

As DAGs **`7_dag_postgres_conn`** e **`8_dag_postgres_hook`** precisam de uma conexão configurada no Airflow para acessar o banco de dados.

1. Acesse a interface web do Airflow (`http://localhost:8080`).
2. No menu superior, vá em **Admin** -> **Connections**.
3. Clique no botão **+** (azul) para adicionar um novo registro.
4. Preencha os campos com os seguintes valores (baseados no `docker-compose.yaml`):

- **Connection Id:** `minha_conexao_postgres`
- **Connection Type:** `Postgres`
- **Host:** `airflow_postgres` (Nome do container do banco)
- **Schema:** `airflow`
- **Login:** `airflow`
- **Password:** `airflow`
- **Port:** `5432`

1. Clique em **Save**.

Agora as DAGs 7 e 8 conseguirão se conectar ao banco de dados para executar suas consultas.

---

## Resolução de Problemas (Troubleshooting)

### Erro de Conexão com Docker Socket (Permission Denied)

Se você encontrar um erro similar a este ao rodar a DAG `6_dag_docker_check`:

```text
ERROR - Failed to establish connection to Docker host unix://var/run/docker.sock: Error while fetching server API version: ('Connection aborted.', PermissionError(13, 'Permission denied')
```

**Causa:** O usuário dentro do container (airflow) não tem permissão para acessar o arquivo `/var/run/docker.sock` do seu computador host, que é necessário para criar novos containers (Docker-in-Docker).

**Solução Rápida (Desenvolvimento Local Linux):**
Dê permissão de leitura/escrita ao socket do Docker no seu computador host:

```bash
sudo chmod 666 /var/run/docker.sock
```

> **Nota:** Em ambientes de produção, essa prática não é recomendada por questões de segurança. O ideal seria adicionar o usuário ao grupo `docker`.

---

## Visão Geral das DAGs

### 1. `1_dag_variables`

- **Conceito:** Uso básico de Variáveis do Airflow.

- **Prática:** Busca valores configurados na UI (Admin > Variables).

### 2. `2_dag_variables_utils`

- **Conceito:** Modularização e Callbacks.

- **Prática:** Usa funções externas e envia alertas (simulados) em caso de sucesso.

### 3. `3_dag_variables_env`

- **Conceito:** Segurança com `.env`.

- **Prática:** Lê credenciais sensíveis via variáveis de ambiente, sem expor no código.

### 4. `4_dag_variables_code`

- **Conceito:** Configuração Estática.

- **Prática:** Usa constantes definidas em arquivos Python (`config.py`).

### 5. `5_dag_api_pipeline`

- **Conceito:** TaskFlow API e ETL.

- **Prática:** Pipeline completo: Extrai (API), Transforma (Pandas) e Carrega (CSV).

### 6. `6_dag_docker_check`

- **Conceito:** Container Efêmero (DockerOperator).

- **Prática:**
  - Cria um container **isolado e temporário** (postgres:13).
  - Este container **NÃO** é o banco de dados do Airflow (`airflow_postgres`). Ele é criado do zero, roda um comando simples e é destruído automaticamente (`auto_remove=True`).
  - Serve para demonstrar como o Airflow pode orquestrar ferramentas em outros ambientes sem instalar nada no worker.

### 7. `7_dag_postgres_conn`

- **Conceito:** PostgresOperator.

- **Prática:** Executa SQL diretamente no banco de metadados.

### 8. `8_dag_postgres_hook`

- **Conceito:** PostgresHook.

- **Prática:** Interage via Python com o banco de dados para buscar e processar registros.

### 9. `9_dag_dynamic_tasks`

- **Conceito:** DAGs Dinâmicas.

- **Prática:** Gera tarefas em loop baseadas em uma configuração.
