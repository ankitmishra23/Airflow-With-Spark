
from airflow import DAG
from datetime import datetime,timedelta
import csv
from airflow.sensors.filesystem import FileSensor
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
import pandas as pd
from sqlalchemy import create_engine
from Operators.postgresCustomOperator import customPostgresOperator
from Sensors.postgresCustomSensor import customPostgresSensor
from airflow.operators.python import BranchPythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.task_group import TaskGroup
from airflow.operators.bash import BashOperator

default_args={
    "start_date":datetime(2022,8,1),
    "owner":"ankit"
}


        


with DAG('student_dag',schedule_interval='@daily',default_args=default_args,catchup=False,tags=['Students','FileSensor'],description='Pipeline on Student data',template_searchpath=['/opt/airflow/files/sql/','/opt/airflow/plugins/']) as dag:
    is_file_present=FileSensor(
        task_id='is_file_present',
        fs_conn_id='student_file_conn',
        filepath='Students_data.csv',
        poke_interval=5,
        timeout=30,
        queue='worker_cpu'
    )

    with TaskGroup(group_id='postgres_tasks') as tg1:
        create_postgres_table=PostgresOperator(
            task_id='create_postgres_table',
            postgres_conn_id='postgres_conn',
            sql='student_ddl.sql',
            queue='worker_cpu'
        )

        load_to_postgres=customPostgresOperator(
            task_id='load_to_postgres',
            conn_id='postgres_conn',
            schemaname='airflow',
            queue='worker_spark',
            filepath='/opt/airflow/datasets/Students_data.csv',
            fileschema={
            "ID":int,
            "class":str,
            "gender":str,
            "race":int,
            "GPA":float,
            "Algebra":int,
            "Calculus1":int,
            "Calculus2":int,
            "Statistics":int,
            "Probability":int,
            "Measure":int,
            "Functional_analysis":int,
            "from1":str,
            "from2":str,
            "from3":str,
            "from4":int,
            "y":int
        },
        tablename='students'
        )

        is_table_loaded=customPostgresSensor(
            task_id='is_table_loaded',
            conn_id='postgres_conn',
            tablename='Students',
            queue='worker_io'
        )
        create_postgres_table>>load_to_postgres>>is_table_loaded


    def choose_action_based_on_sensor(**kwargs):
        value=kwargs['ti'].xcom_pull(key='postgres_sensor_value')
        if value=='True':
            return 'processing_data'
        else:
            return 'table_not_found'


    choose_action=BranchPythonOperator(
        task_id='choose_action',
        python_callable=choose_action_based_on_sensor,
        queue='worker_spark'
    )

    processing_data=BashOperator(task_id='processing_data',queue='worker_io',bash_command='echo Hello',do_xcom_push=False)
    table_not_found=BashOperator(task_id='table_not_found',queue='worker_cpu',bash_command='echo World',do_xcom_push=False)

    is_file_present>>tg1>>choose_action>>[processing_data,table_not_found]

