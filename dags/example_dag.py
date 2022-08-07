from airflow import DAG
import datetime
from airflow.operators.dummy import DummyOperator
from airflow.operators.bash import BashOperator

default_args={
    "start_date":datetime.datetime(2022,8,1),
    "owner":"ankit"
}

with DAG("example",schedule_interval='@daily',default_args=default_args,catchup=False,tags=['example'],description="This is an example dag.") as dag:
    task1=DummyOperator(task_id="task1")
    task2=DummyOperator(task_id="task2")
    bashtask1=BashOperator(task_id="bashtask1",bash_command="echo Hello World")

    task1>>task2>>bashtask1
