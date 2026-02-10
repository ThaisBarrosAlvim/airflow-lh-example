import pendulum
from airflow.decorators import dag, task
from utils.config import TABLES_CONFIG

default_args = {
    'owner': 'thais_alvim',
    'depends_on_past': False,
    'email': ['email@exemplo.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'start_date': pendulum.datetime(2026, 1, 1, tz="UTC"),
}

@dag(
    dag_id='9_dag_dynamic_tasks',
    default_args=default_args,
    description='DAG dinâmica gerando tasks com base em lista de configuração',
    schedule=None,
    catchup=False,
    tags=['dynamic', 'loops'],
)
def dynamic_workflow():

    @task
    def start_pipeline():
        print("Iniciando o pipeline dinâmico.")

    # Template de exemplo de processamento que será reutilizado
    @task
    def process_table(table_name: str):
        print(f"Echo: simulando processamento para a tabela [{table_name}]")
        return f"{table_name} processada"

    @task
    def end_pipeline():
        print("Todas as tabelas foram processadas. Pipeline finalizado.")

    
    # Lista vazia para agrupar as tasks
    my_dynamic_tasks = []

    for table_name in TABLES_CONFIG:
        task_instance = process_table.override(task_id=f'process_table_{table_name}')(table_name=table_name)
        
        # Sem conexão com o fluxo ainda
        my_dynamic_tasks.append(task_instance)

    # Fluxo completo
    start_pipeline() >> my_dynamic_tasks >> end_pipeline()

dag_instance = dynamic_workflow()
