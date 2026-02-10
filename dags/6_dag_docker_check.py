import pendulum
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator

default_args = {
    'owner': 'thais_alvim',
    'depends_on_past': False,
    'email': ['email@exemplo.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    # 'retries': 1,
    # 'retry_delay': timedelta(minutes=5),
    'start_date': pendulum.datetime(2026, 1, 1, tz="UTC"),
}

with DAG(
    dag_id='6_dag_docker_check',
    default_args=default_args,
    description='Verifica versão do Postgres usando DockerOperator (Docker-in-Docker)',
    schedule=None,
    catchup=False,
    tags=['docker'],
) as dag:

    # Task que sobe um container pontual apenas para rodar este comando
    # IMPORTANTE: Este container é "efêmero", ou seja, ele é criado, executa o comando e depois é destruído (auto_remove=True).
    # Ele NÃO está se conectando ao container 'airflow_postgres' que mantém o banco de dados do Airflow.
    # Ele é um container isolado, puro, apenas da imagem postgres:13, servindo como exemplo de execução isolada.
    check_postgres_version = DockerOperator(
        task_id='check_postgres_version',
        image='postgres:13',
        container_name='task_check_postgres_version',
        api_version='auto',
        auto_remove=True,
        command="sh -c 'echo Executando tarefa dentro de um container postgres, versão atual: && postgres --version'",
        docker_url='unix://var/run/docker.sock',
        network_mode='bridge',
    )

    check_postgres_version
