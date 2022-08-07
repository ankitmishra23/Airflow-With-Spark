
from airflow.models.baseoperator import BaseOperator
from Hooks.postgresCustomHook import customPostgresHook
import pandas as pd
import psycopg2
import numpy as np

class customPostgresOperator(BaseOperator):
    def __init__(self,conn_id,schemaname,filepath,fileschema,tablename,**kwargs):
        super().__init__(**kwargs)
        self.conn_id=conn_id
        self.schemaname=schemaname
        self.filepath=filepath
        self.file_schema=fileschema
        self.tablename=tablename

    def execute(self,context):
        conn=customPostgresHook(self.conn_id).get_custom_connection()
        cursor=conn.cursor()
        df=pd.read_csv(self.filepath,dtype=self.file_schema)
        tuples=[tuple(x) for x in df.to_numpy()]
        cols=','.join(list(df.columns))
        psycopg2.extras.execute_values(cursor,'insert into %s(%s) values %%s'%(self.tablename,cols),tuples)
        conn.commit()
        return "data loaded to postgres."

