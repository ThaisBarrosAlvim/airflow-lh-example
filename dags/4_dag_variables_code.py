import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator
from utils.config import VARIAVEL_TESTE

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

def print_variable_from_code():
    # A variável VARIAVEL_TESTE já vem do import
    print(f"O valor da variável definida no código e importada é: {VARIAVEL_TESTE}")

with DAG(
    dag_id='4_dag_variables_code',
    default_args=default_args,
    description='Variáveis via código (config.py)',
    schedule=None,
    catchup=False,
    tags=['variables'],
) as dag:

    task_print_var_code = PythonOperator(
        task_id='print_variable_code',
        python_callable=print_variable_from_code,
    )

