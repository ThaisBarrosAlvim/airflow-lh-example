import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable

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

def print_variable_task():
    my_var = Variable.get("MY_VAR", default_var="Valor Padrão (Fallback)")
    print(f"O valor da variável buscando diretamente é: {my_var}")

with DAG(
    dag_id='1_dag_variables',
    default_args=default_args, # Argumentos padrões para toda task da DAG
    description='Variáveis diretamente do Airflow',
    schedule=None,
    catchup=False, # Impede que o Airflow tente rodar execuções passadas
    tags=['variables'],
) as dag:

    task_print_var = PythonOperator(
        task_id='print_variable',
        python_callable=print_variable_task,
    )
