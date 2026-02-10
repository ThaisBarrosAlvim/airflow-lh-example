import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator

from utils.variable_utils import get_airflow_variable
from utils.email import success_callback

default_args = {
    'owner': 'thais_alvim',
    'depends_on_past': False, # Se True, a task depende do sucesso da execução anterior
    'email': ['email@exemplo.com'], # Lista de e-mails para notificações
    'email_on_failure': False, # Enviar e-mail quando a task falha
    'email_on_retry': False, # Enviar e-mail quando a task tenta rodar novamente
    # 'retries': 1,
    # 'retry_delay': timedelta(minutes=5), 
    'start_date': pendulum.datetime(2026, 1, 1, tz="UTC"),
    # 'on_success_callback': success_callback # Callback que será utilizado para cada task
}

def print_variable_from_utils():
    my_var = get_airflow_variable("MY_VAR", fallback="Fallback via Utils")
    print(f"O valor da variável via função utilitária é: {my_var}")

with DAG(
    dag_id='2_dag_variables_utils',
    default_args=default_args,
    description='Variáveis via função utilitária',
    schedule=None,
    catchup=False,
    tags=['variables', 'utils'],
    on_success_callback=success_callback # Callback chamado na conclusão da DAG
) as dag:

    task_print_var_utils = PythonOperator(
        task_id='print_variable_utils',
        python_callable=print_variable_from_utils,
    )
