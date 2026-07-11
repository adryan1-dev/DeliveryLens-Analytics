# 🚚 DeliveryLens Analytics

![Data Engineering](https://img.shields.io/badge/Data%20Engineering-Pipeline-blue)
![Python](https://img.shields.io/badge/Python-3.12-yellow)
![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-2.10.4-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)

## 📌 Sobre o Projeto

O **DeliveryLens Analytics** é uma plataforma de engenharia de dados desenvolvida para simular um ambiente real de processamento analítico de uma empresa de delivery.

O objetivo do projeto é construir uma pipeline completa de dados, desde a ingestão de dados através de uma API REST até a disponibilização dos dados em um banco analítico, utilizando boas práticas de Engenharia de Dados.

O projeto aplica conceitos utilizados no mercado como:

* Arquitetura de pipelines de dados (Medallion Architecture)
* Orquestração de workflows
* Processamento e transformação de dados
* Persistência em banco relacional
* Containerização
* Organização modular de código

---

# 🏗️ Arquitetura da Pipeline
             API REST
                |
                ↓
      Python Data Ingestion
                |
                ↓
          Apache Airflow
                |
                ↓
          Bronze Layer (dados brutos)
                |
                ↓
          Silver Layer (dados validados)
                |
                ↓
         PostgreSQL Database
                |
                ↓
      Analytics / BI Layer

---

# 🔄 Fluxo do Pipeline

## 1. Data Ingestion

A pipeline realiza a coleta dos dados através de uma API REST utilizando Python.

Responsável por:

* Realizar chamadas HTTP
* Validar respostas
* Capturar dados brutos
* Preparar dados para processamento

Tecnologias:

* Python
* Requests API

---

## 2. Bronze Layer

Camada responsável por salvar o dado exatamente como chegou da fonte, sem nenhuma transformação.

Motivação: em ambientes reais, nunca devemos perder o dado original. A Bronze serve para auditoria, reprocessamento, histórico e recuperação em caso de falha nas camadas seguintes.

Responsável por:

* Salvar o JSON bruto retornado pela API
* Persistir os dados fora do container, via volume Docker

Arquivo gerado:
data/bronze/users_<data>.json

---

## 3. Silver Layer

Camada responsável por validar os registros vindos da Bronze, sem descartar dados.

Cada registro é lido do arquivo Bronze mais recente e passa por validações de:

* `id` presente
* `name` presente e não vazio
* `email` presente e com formato válido

Cada registro recebe dois campos adicionais:

* `is_valid`: `true` ou `false`
* `validation_errors`: lista com os motivos de invalidação (vazia se o registro for válido)

Nenhum registro é descartado nessa etapa — inválidos são mantidos e sinalizados, para investigação posterior.

Arquivo gerado:
data/silver/users_<data>.json

---

## 4. Orquestração com Apache Airflow

O workflow é gerenciado pelo Apache Airflow.

A DAG é responsável por:

* Controlar execução do pipeline
* Gerenciar tarefas
* Registrar logs
* Monitorar falhas

Fluxo da DAG:
Start
|
↓
Run Delivery Pipeline
|
↓
Extract API Data
|
↓
Save Bronze
|
↓
Transform to Silver
|
↓
Load PostgreSQL
|
↓
Finish

---

## 5. Data Storage

Os dados são armazenados utilizando PostgreSQL.

Modelo inicial:
deliverylens
│
└── deliveries_test
│
├── id
├── user_id
├── name
├── username
└── email

---

# 🛠️ Tecnologias Utilizadas

## Linguagens

* Python

## Banco de Dados

* PostgreSQL 16

## Orquestração

* Apache Airflow 2.10.4

## Infraestrutura

* Docker
* Docker Compose

## Bibliotecas Python

* Requests
* Psycopg2

---

# 📂 Estrutura do Projeto
DeliveryLens-Analytics/
│
├── airflow/
│   └── dags/
│       └── deliverylens_pipeline.py
│
├── src/
│   │
│   ├── ingestion/
│   │   └── api_ingestion.py
│   │
│   ├── bronze/
│   │   └── bronze_loader.py
│   │
│   ├── silver/
│   │   └── silver_transformer.py
│   │
│   ├── pipeline/
│   │   └── delivery_pipeline.py
│   │
│   ├── db/
│   │   ├── connection.py
│   │   └── repository.py
│   │
│   └── config/
│       └── settings.py
│
├── data/               # dados gerados pelo pipeline (ignorado no Git)
│   ├── bronze/
│   └── silver/
│
├── docker-compose.yml
├── requirements.txt
└── README.md

---

# 🐳 Executando o Projeto

## Pré-requisitos

Necessário possuir:

* Docker
* Docker Compose
* Git

---

## 1. Clone o repositório

```bash
git clone https://github.com/adryan1-dev/DeliveryLens-Analytics.git

cd DeliveryLens-Analytics
```

---

## 2. Configure as variáveis de ambiente

Crie um arquivo:
.env

Exemplo:

```env
DB_NAME=deliverylens
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432

API_URL=https://jsonplaceholder.typicode.com/users
API_TIMEOUT=10
```

---

## 3. Suba os containers

```bash
docker compose up -d
```

Serviços iniciados:

| Serviço           | Porta |
| ----------------- | ----- |
| Airflow Webserver | 8080  |
| PostgreSQL        | 5433  |

---

## 4. Acesse o Airflow

Abra:
http://localhost:8080

Execute a DAG:
deliverylens_pipeline

---

# 🧪 Testando a Pipeline

Também é possível executar diretamente pelo terminal:

```bash
docker compose exec airflow-scheduler \
airflow dags test deliverylens_pipeline 2026-07-11
```

Resultado esperado:
Silver Layer: X registros validos, Y invalidos
Pipeline executada com sucesso!
DagRun Finished
state: success

Após a execução, os dados ficam disponíveis em:
data/bronze/users_<data>.json   # dado bruto, como veio da API
data/silver/users_<data>.json   # dado validado, com is_valid e validation_errors

---

# 📊 Próximas Evoluções

O projeto está sendo desenvolvido seguindo uma evolução próxima de ambientes reais.

Roadmap:

## ✅ Sprint 1 - Fundamentos

* [x] Estrutura inicial do projeto
* [x] API ingestion
* [x] PostgreSQL
* [x] Organização modular

## ✅ Sprint 2 - Orquestração

* [x] Docker Compose
* [x] Apache Airflow
* [x] Criação da DAG
* [x] Execução automatizada

## 🚧 Sprint 3 - Arquitetura Medalhão

Implementação:
Bronze Layer  ✅
|
↓
Silver Layer  ✅
|
↓
Gold Layer    🚧

* [x] Bronze Layer: persistência do dado bruto (JSON) via `save_bronze()`
* [x] Volume Docker para persistir dados fora do container
* [x] Silver Layer: validação de registros (`id`, `name`, `email`), com `is_valid` e `validation_errors`
* [ ] Conectar Silver ao carregamento no PostgreSQL
* [ ] Gold Layer: modelagem dimensional (Star Schema)

---

## 🚧 Sprint 4 - Airflow Profissional

Planejado:

* Separar DAG em tasks (`task_ingestion`, `task_bronze`, `task_silver`, `task_gold`)
* Retries e tratamento de falhas
* Parâmetros e schedule configuráveis

---

## 🚧 Sprint 5 - Cloud & Analytics

Planejado:

* AWS S3 / MinIO
* Data Lake
* dbt
* Parquet
* Data Warehouse
* CI/CD
* Dashboard BI

---

# 🎯 Objetivo Profissional

Este projeto foi desenvolvido como estudo prático de Engenharia de Dados, aplicando conceitos utilizados em ambientes profissionais para construção de pipelines escaláveis e confiáveis.

---

# 👨‍💻 Autor

**Adryan Chaves**

Estudante de Engenharia de Dados / Desenvolvimento de Sistemas

Foco em:

* Python
* SQL
* ETL/ELT
* Data Pipelines
* Cloud Computing
* Analytics Engineering

---

⭐ Se este projeto foi útil, considere deixar uma estrela no repositório!