from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

def execute_daily(**kwargs):
    print("Ejecutando tarea diaria")
    main(date_limit="daily")

def execute_historical(**kwargs):
    execution_date = kwargs['execution_date']
    if execution_date.year % 10 == 0:  # Cambia esto según tus necesidades
        print("Ejecutando tarea histórica")
        main(date_limit="historical")
    else:
        print("Saltando tarea histórica")

# Configuración de DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define la fecha de inicio para que sea dentro de 2 horas a partir de ahora
start_date = datetime.now() + timedelta(hours=2)

dag = DAG(
    'submit_forms',
    default_args=default_args,
    description='Submit forms',
    schedule_interval=timedelta(days=1),  # Ejecución diaria del DAG
    start_date=start_date,
    catchup=False,
)

# Tarea para ejecutar main_daily.py diariamente
t1 = PythonOperator(
    task_id='run_daily',
    python_callable=execute_daily,
    provide_context=True,  # Necesario para pasar kwargs
    dag=dag,
)

# Tarea para ejecutar main_historical.py
t2 = PythonOperator(
    task_id='run_historical',
    python_callable=execute_historical,
    provide_context=True,  # Necesario para pasar kwargs
    dag=dag,
)

# Configuración de dependencias
t1 >> t2
