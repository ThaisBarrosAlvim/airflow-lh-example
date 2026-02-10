import os
import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator
from dotenv import load_dotenv

default_args = {
    'owner': 'thais_alvim',
    'depends_on_past': False, # Se True, a task depende do sucesso da execução anterior
    'email': ['email@exemplo.com'], # Lista de e-mails para notificações
    'email_on_failure': False, # Enviar e-mail quando a task falha
    'email_on_retry': False, # Enviar e-mail quando a task tenta rodar novamente
    # 'retries': 1,
    # 'retry_delay': timedelta(minutes=5),
    'start_date': pendulum.datetime(2026, 1, 1, tz="UTC"),
}

def print_variable_from_env():
    # Carrega as variáveis do arquivo .env mapeado via docker-compose (/opt/airflow/.env)
    load_dotenv(dotenv_path='/opt/airflow/.env')
    
    # Busca a variável de ambiente com os.getenv e define um fallback
    my_var = os.getenv("TESTE_VARIAVEL", "Fallback do Ambiente")
    print(f"O valor da variável carregada do .env é: {my_var}")

with DAG(
    dag_id='3_dag_variables_env',
    default_args=default_args,
    description='Variáveis via arquivo .env usando python-dotenv',
    schedule=None,
    catchup=False,
    tags=['variables'],
) as dag:

    task_print_var_env = PythonOperator(
        task_id='print_variable_env',
        python_callable=print_variable_from_env,
    )
