from airflow.utils.email import send_email

def success_callback(context):
    dag = context.get('dag')
    
    # Pega os emails definidos no default_args da DAG
    recipient_emails = dag.default_args.get('email')

    subject = f"Airflow Success: {dag.dag_id}"
    html_content = f"""
    <h3>A DAG {dag.dag_id} finalizou com sucesso.</h3>
    <p>Data de execução: {context['execution_date']}</p>
    """
    
    print(f"Sending email to: {recipient_emails}")
    send_email(recipient_emails, subject, html_content)
