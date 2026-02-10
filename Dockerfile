FROM apache/airflow:2.10.2-python3.11

# Alternar para usuário 'airflow' para instalar dependências
USER airflow

COPY requirements.txt .

# Instalar dependências listadas no requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
