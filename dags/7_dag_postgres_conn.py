import pendulum
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator

default_args = {
    'owner': 'thais_alvim',
    'depends_on_past': False,
    'start_date': pendulum.datetime(2026, 1, 1, tz="UTC"),
}

with DAG(
    dag_id='7_dag_postgres_conn',
    default_args=default_args,
    description='Consulta dados da Metastore (Postgres interno)',
    schedule=None,
    catchup=False,
    tags=['database', 'postgres'],
) as dag:

    # Verifica a versão do Postgres (sem output, só "Rows affected: 1")
    check_version = PostgresOperator(
        task_id='check_postgres_version',
        postgres_conn_id='minha_conexao_postgres',
        sql="SELECT version();"
    )

    # Consulta a tabela interna 'dag_run' (sem output, só "Rows affected: 5")
    get_latest_runs = PostgresOperator(
        task_id='get_latest_dag_runs',
        postgres_conn_id='minha_conexao_postgres',
        sql="""
            SELECT dag_id, run_id, state, execution_date 
            FROM dag_run 
            ORDER BY execution_date DESC 
            LIMIT 5;
        """
    )

    check_version >> get_latest_runs
