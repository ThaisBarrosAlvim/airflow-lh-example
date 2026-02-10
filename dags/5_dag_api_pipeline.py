import pendulum
from datetime import timedelta
from airflow.decorators import dag, task
from airflow.models import Variable
import requests
import pandas as pd
import os

default_args = {
    'owner': 'thais_alvim',
    'depends_on_past': False, # Se True, a task depende do sucesso da execução anterior
    'email': ['email@exemplo.com'], # Lista de e-mails para notificações
    'email_on_failure': False, # Enviar e-mail quando a task falha
    'email_on_retry': False, # Enviar e-mail quando a task tenta rodar novamente
    # 'retries': 1, # Sem retry para a DAG inteira
    # 'retry_delay': timedelta(minutes=5),
    'start_date': pendulum.datetime(2026, 1, 1, tz="UTC"),
}

@dag(
    dag_id='5_dag_api_pipeline',
    default_args=default_args,
    description='Pipeline de extração de API pública e salvamento em CSV',
    schedule=None,
    catchup=False,
    tags=['api', 'pandas'],
)
def api_pipeline():

    @task(retries=3, retry_delay=timedelta(seconds=10))
    def extract_data():
        # Busca a URL da variável ou usa o default
        api_url = Variable.get("API_URL", default_var="https://randomuser.me/api/")
        print(f"Buscando dados de: {api_url}")
        
        params = {"nat": "br", "results": 5}
        response = requests.get(api_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Retorna o dicionário completo (XCom automático)
        return data

    @task
    def transform_data(json_data: dict):
        results = json_data.get('results', [])
        processed_data = []

        for user in results:
            processed_user = {
                'first_name': user['name']['first'],
                'last_name': user['name']['last'],
                'email': user['email'],
                'country': f"{user['location']['country']}+MOD" # Transformação simples
            }
            processed_data.append(processed_user)
        
        print(f"Dados transformados: {len(processed_data)} registros.")
        return processed_data

    @task
    def save_data(user_list: list):
        if not user_list:
            print("Nenhum dado para salvar.")
            return

        df = pd.DataFrame(user_list)
        
        output_dir = "/opt/airflow/outputs" # Diretorio de saida
        os.makedirs(output_dir, exist_ok=True)
        
        file_path = os.path.join(output_dir, "users.csv")
        
        # Salva em CSV com cabeçalho
        df.to_csv(file_path, index=False, header=True)
        print(f"Arquivo salvo com sucesso em: {file_path}")

    # Definição do fluxo
    raw_data = extract_data()
    transformer_data = transform_data(raw_data)
    save_data(transformer_data)

# Instancia a DAG
dag_instance = api_pipeline()
