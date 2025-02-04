from airflow import DAG
from airflow.operators.bash_operator import BashOperator

# other packages
from datetime import timedelta
from datetime import datetime
from airflow.utils.dates import days_ago

default_args = {'owner': 'santiago','depends_on_past': False,'email_on_failure': False,'email_on_retry': False,
                'retries': 2,'retry_delay': timedelta(seconds=60)}

dag = DAG(dag_id='ETL_PROCESAMIENTO_HTML',
          description='ETL para procesar archivos HTML',
          default_args=default_args,
          start_date=datetime(2024, 10, 27, 1, 00, 00), 
          schedule_interval='0 * * * *',
          catchup=False,
          concurrency=1,
          dagrun_timeout=timedelta(hours=3),
          tags=['ETL', 'Laboratorio'])

task_1 = BashOperator(
    task_id='SCRIPT_PROCESAMIENTO_HTML',
    bash_command='/root/miniconda3/envs/htmlProcess/bin/python  /data/prueba-tecnica-ingeniero-datos/ETLProccess/ETL_transactions.py',
    dag=dag,
)