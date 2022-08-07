
from airflow.hooks.base import BaseHook
import psycopg2
import psycopg2.extras

class customPostgresHook(BaseHook):
    def __init__(self,conn_id,**kwargs):
        super().__init__(**kwargs)
        self.conn_id=conn_id


    def get_custom_connection(self):
        uri=BaseHook.get_connection(self.conn_id)
        conn=psycopg2.connect(database=uri.schema,user=uri.login,password=uri.password,host=uri.host,port=uri.port)
        return conn

        
        
