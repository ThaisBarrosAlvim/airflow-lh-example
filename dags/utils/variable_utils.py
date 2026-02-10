from airflow.models import Variable

def get_airflow_variable(var_name, fallback="Fallback Value"):
    """
    Busca uma variável do Airflow pelo nome.
    Caso não exista, retorna o valor de fallback definido.
    """
    return Variable.get(var_name, default_var=fallback)

