import os
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from datetime import datetime, timedelta
from dotenv import load_dotenv
import requests

load_dotenv()

# Variáveis de ambiente
DBT_DIR = os.getenv('DBT_DIR')
MEU_EMAIL = os.getenv('MEU_EMAIL')
SCRIPTS_PATH = os.getenv('SCRIPTS_PATH')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


default_args = {
    "owner": "Vanessa",
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}

def generate_data():
    """Executa o script para gerar dados fake"""
    os.system(f"python {SCRIPTS_PATH} generate_fake_data.py")


with DAG(
    dag_id="ecommerce_analytics_dag",
    start_date=datetime(2025, 1, 1),
    schedule="@weekly",
    catchup=False,
    default_args=default_args,
    tags=["ecommerce", "dbt", "churn"],
) as dag:

    t1_generate_data = PythonOperator(
        task_id="generate_fake_data",
        python_callable=generate_data
    ) 

    t2_dbt_seed = BashOperator(
        task_id="dbt_seed",
        bash_command=f"cd {DBT_DIR} && dbt seed --profiles-dir /usr/local/airflow/include/.dbt"
    )

    t3_dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"cd {DBT_DIR} && dbt run --profiles-dir /usr/local/airflow/include/.dbt"
    )

    t4_dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"cd {DBT_DIR} && dbt test --profiles-dir /usr/local/airflow/include/.dbt"
    )

    t5_generate_report = BashOperator(
        task_id="generate_report",
        bash_command=f"python {os.path.join(SCRIPTS_PATH, 'generate_report.py')}"
    )


    t1_generate_data >> t2_dbt_seed >> t3_dbt_run >> t4_dbt_test >> t5_generate_report