from airflow.sensors.base import BaseSensorOperator
import psycopg2
from Hooks.postgresCustomHook import customPostgresHook

class customPostgresSensor(BaseSensorOperator):
    def __init__(self,conn_id,tablename,**kwargs):
        super().__init__(**kwargs)
        self.conn_id=conn_id
        self.tablename=tablename
        

    def poke(self,context):
        conn=customPostgresHook(conn_id=self.conn_id).get_custom_connection()
        cursor=conn.cursor()
        cursor.execute(f"select to_regclass('{self.tablename}')")
        response={}
        response['value']=cursor.fetchone()
        if not response['value']:
            context['ti'].xcom_push(key='postgres_sensor_value',value='False')
            return False
        else:
            if str(response['value'][0]) in ('0',''):
                context['ti'].xcom_push(key='postgres_sensor_value',value='False')
                return False
        conn.commit()
        conn.close()
        context['ti'].xcom_push(key='postgres_sensor_value',value='True')
        return True
