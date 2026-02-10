import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

default_args = {
    'owner': 'thais_alvim',
    'depends_on_past': False,
    'start_date': pendulum.datetime(2026, 1, 1, tz="UTC"),
}

def fetch_and_print_data():
    # Instancia o Hook conectando na connection
    pg_hook = PostgresHook(postgres_conn_id='minha_conexao_postgres')
    
    sql_query = """
        SELECT dag_id, run_id, state, execution_date 
        FROM dag_run 
        ORDER BY execution_date DESC 
        LIMIT 5;
    """
    
    # Usa o método .get_records() para buscar os dados (retorna uma lista de tuplas)
    records = pg_hook.get_records(sql_query)
    # Aqui acontece a query e tem a saida nos logs de: "Rows affected: 5"
    
    print(f"Extração dos registros via hook: ({len(records)} registros)")
    
    for row in records: # (dag_id, run_id, state, execution_date)
        dag_id = row[0]
        state = row[2]
        print(f"DAG: {dag_id} | Status: {state} | Dados brutos: {row}")

with DAG(
    dag_id='8_dag_postgres_hook',
    default_args=default_args,
    description='Usa PostgresHook para buscar e printar dados',
    schedule=None,
    catchup=False,
    tags=['database', 'hook'],
) as dag:

    task_fetch_data = PythonOperator(
        task_id='fetch_data_with_hook',
        python_callable=fetch_and_print_data,
    )
