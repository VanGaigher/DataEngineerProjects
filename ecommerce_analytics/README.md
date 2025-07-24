# 📘 Documentação do Projeto: E-commerce Analytics com dbt e Airflow

## 🎯 Visão Geral do Projeto

Este projeto tem como objetivo principal o desenvolvimento e implementação de um pipeline de engenharia de dados analítico moderno, focado em **análise de vendas** e **previsão de churn** para um e-commerce simulado. A solução integra ferramentas como **dbt** para modelagem de dados e **Apache Airflow (via Astro CLI)** para orquestração, culminando na geração de **relatórios semanais automatizados**.

-----

## 🧱 Estrutura do Repositório

O repositório do projeto está organizado para otimizar a clareza e a manutenção dos componentes:

```
ecommerce_analytics/
├── airflow/            # Contém as definições de DAGs e operadores customizados do Airflow.
├── dbt/                # Abriga o projeto dbt, incluindo modelos de dados, testes e seeds.
├── scripts/            # Scripts utilitários para geração de dados fictícios.
├── reports/            # Templates para a geração dos relatórios HTML.
├── pyproject.toml      # Lista de dependências Python do projeto.
└── README.md           # Documentação principal do projeto (este arquivo).
```

-----

## ✅ Etapas de Implementação

As seguintes etapas detalham o processo de configuração e desenvolvimento do pipeline:

### 1\. Configuração do Ambiente

Para iniciar o desenvolvimento, é essencial preparar o ambiente com as ferramentas necessárias:

  * **Instalação do Astro CLI:**
    Siga as instruções oficiais para instalar o Astro CLI, que facilitará a orquestração local do Airflow:
    ```bash
    https://www.astronomer.io/docs/astro/cli/install-cli
    ```
  * **Inicialização do Projeto Astro:**
    Crie a estrutura básica do projeto Airflow utilizando o Astro CLI:
    ```bash
    astro dev init
    ```
  * **Configuração do Ambiente Virtual/Container:**
    Crie e ative um ambiente virtual (ou utilize um container Docker) e instale as dependências Python listadas em `pyproject.toml`:
      * `dbt-core` e `dbt-duckdb` (Optamos por usar um banco de dados local)
      * `apache-airflow`
      * `faker` (para geração de dados)
      * `jinja2` (para templating de relatórios)
      * `pandas` (para manipulação de dados)

### 2\. Geração de Dados Fictícios

O projeto utiliza dados simulados para replicar um cenário de e-commerce:

  * **Script:** `scripts/generate_fake_data.py`
  * **Funcionalidade:** Este script é responsável por gerar os seguintes conjuntos de dados fictícios em formato CSV:
      * `customers.csv`
      * `orders.csv`
      * `products.csv`
      * `order_items.csv`
      * `cancelamentos.csv`
  * **Armazenamento:** Os arquivos CSV gerados devem ser armazenados no diretório `dbt/seeds/`, permitindo que sejam carregados no Data Warehouse via `dbt seed`.

### 3\. Configuração do Projeto dbt

O projeto dbt (`dbt/`) é a camada de transformação e modelagem de dados:

  * **Inicialização:**
    Inicie o projeto dbt no diretório `dbt/`:

    ```bash
    dbt init ecommerce_analytics
    ```
  * **Criação do profile.yml**
  Crie dentro do arquivo de instalação do .dbt o profiles.yml da seguinte maneira:

    ```bash
    dbt_ecommerce:
    target: dev
    outputs:
      dev:
        type: duckdb
        path: data/dbt_ecommerce.duckdb  # banco local em arquivo .duckdb
        schema: staging
    ```
  

  * **Carregamento de Seeds:**
    Após colocar os arquivos CSV gerados em `dbt/seeds/`, execute o comando para carregar os dados no seu Data Warehouse:

    ```bash
    dbt seed
    ```
  

  * **Modelagem de Dados (Camadas):**
    Os modelos dbt são organizados em três camadas distintas para garantir modularidade e clareza:

      * **Staging (`models/staging/`):** Modelos brutos que padronizam e limpam os dados das fontes.
          * `stg_customers.sql`
          * `stg_orders.sql`
          * `stg_products.sql`
      * **Intermediate (`models/intermediate/`):** Modelos que realizam transformações intermediárias complexas, servindo de base para os marts.
          * `int_churn_prediction_data.sql`
      * **Marts (`models/marts/`):** Modelos agregados e prontos para consumo por ferramentas de BI e relatórios.
          * `fct_sales.sql` (Fato de vendas)
          * `dim_customer.sql` (Dimensão de clientes)
          * `dim_product.sql` (Dimensão de produtos)

  * **Testes de Qualidade de Dados:**
    Implemente testes de dbt (e.g., `not_null`, `unique`) nos modelos para garantir a integridade e a qualidade dos dados. Execute os testes com:

  Para isto, dentro de cada pasta das camadas crie o arquivo schema.yml com os testes.
  
  Após criado, rode:

  ```bash
  dbt test
  ```
    
### 4\.Visualização na interface gráfica:

Você consegue visualizar as informações e dados das tabelas, usando o comando:
```
dbt docs generate
dbt docs serve
```
Estes comandos vão gerar documentação e você poderá ver a estrutura dos dados.

### 5\. Criação da DAG no Airflow

A orquestração do pipeline é realizada através de uma Directed Acyclic Graph (DAG) no Airflow:

  * **Localização:** `airflow/dags/ecommerce_dag.py`
  * **Tarefas (Tasks):** A DAG deve incluir as seguintes tarefas, executadas em sequência lógica:
      * `generate_data`: Invoca o script de geração de dados fictícios.
      * `load_to_warehouse`: (Opcional, se a carga inicial não for feita pelo `dbt seed` ou requerer um passo ETL separado).
      * `dbt_seed`: Executa o comando `dbt seed` para carregar dados iniciais.
      * `dbt_run`: Executa os modelos dbt para transformar os dados.
      * `dbt_test`: Roda os testes de qualidade dos dados após a transformação.
      * `send_report`: Gera o relatório semanal e o envia (e.g., por e-mail).
  * **Agendamento:** A DAG deve ser agendada para execução **semanal** (`@weekly`).

### 6\. Relatório HTML Semanal

Um relatório consolidado é gerado semanalmente para análise das métricas de negócio:

  * **Localização:** `reports/weekly_report.html` (template)
  * **Tecnologia:** Utilização do Jinja2 para templating dinâmico, permitindo a inserção de dados calculados pelos modelos dbt.
  * **Conteúdo:** O relatório deve incluir as seguintes métricas e informações:
      * Total de vendas do período.
      * Produtos com maior margem de lucro.
      * Taxa de churn de clientes.
      * Ticket médio por categoria de produto.

### 7\. Execução e Validação

Após a implementação das etapas anteriores, é crucial validar o funcionamento do pipeline:

  * **Execução Local:** Execute o pipeline completo utilizando o Astro CLI no ambiente local para simular a produção.
  * **Validação dbt:** Verifique os resultados dos modelos dbt no seu Data Warehouse para garantir que os dados estão corretos e as transformações foram aplicadas adequadamente.
  * **Teste de Envio de Relatório:** Confirme se o relatório HTML é gerado corretamente e se o mecanismo de envio (e.g., e-mail) funciona conforme o esperado.

-----

## 📌 KPIs do Projeto

As métricas chave de desempenho (KPIs) monitoradas por este projeto, juntamente com suas respectivas fontes no projeto dbt, são as seguintes:

| Métrica                   | Fonte dbt                 | Descrição                                                                       |
| :------------------------ | :------------------------ | :------------------------------------------------------------------------------ |
| Receita total             | `fct_sales`               | Soma do valor total das vendas realizadas no período.                           |
| Ticket médio por categoria | `fct_sales` + `dim_product` | Valor médio das vendas, segmentado pelas categorias de produtos.                |
| Produtos com maior margem | `dim_product`             | Identifica os produtos que geram maior lucro bruto para o e-commerce.           |
| Taxa de churn             | `dim_customer`            | Percentual de clientes que cancelaram suas contas ou deixaram de comprar.       |
| Clientes fiéis            | `int_churn_prediction_data` | Identifica clientes com alta frequência de compra ou longo histórico no e-commerce. |

-----

## 🎁 Funcionalidades Adicionais (Opcionais)

Para aprimorar ainda mais o projeto, as seguintes funcionalidades podem ser exploradas:

  * **Painel de BI:** Integração com ferramentas de Business Intelligence como Metabase, Looker Studio ou dashboards interativos construídos com Streamlit para visualização dos KPIs.
  * **Alertas Automatizados:** Configuração de alertas por e-mail (ou outras plataformas de notificação) quando a taxa de churn exceder um determinado limite.
  * **Dashboards Temporais:** Implementação de dashboards que mostrem a evolução dos KPIs ao longo do tempo (e.g., últimos 30 dias, 6 meses), permitindo análises de tendência.

-----