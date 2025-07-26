FROM astrocrpublic.azurecr.io/runtime:3.0-5

# Instala dbt e adapta o Python compatível
RUN pip install dbt-core==1.9.0 dbt-postgres==1.9.0

# Instala o Git (evita o erro do dbt debug)
USER root
RUN apt-get update && apt-get install -y git

# Garante que o diretório .dbt exista e copia o profiles.yml para o local certo
RUN mkdir -p /home/astro/.dbt
COPY include/.dbt/profiles.yml /home/astro/.dbt/profiles.yml

# Copia os arquivos do projeto (opcional, se aplicável)
COPY reports /usr/local/airflow/reports

USER astro
