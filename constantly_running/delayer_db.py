import psycopg2
import os 
import pytz
import sys
from datetime import datetime
from random import randint


class Delayer():

    def __init__(self,conn,cursor):
        self.connection = conn
        self.cursor = cursor 

    def get_fields(self):
        return  [
                'delayer_db_internal_tag',
                'lead_id',
                'delayer_db_internal_comment',
                'trigger_date',
                'additional_info'
            ]

    def add_record(self,**kwargs):
        db_fields = {
                'delayer_db_internal_tag':None,
                'lead_id':None,
                'delayer_db_internal_comment':None,
                'trigger_date':None,
                'additional_info':None
            }
        for key in db_fields.keys():
            if key in dict(kwargs.items()):
                db_fields[key] = dict(kwargs.items())[key]                   
        if any(map(lambda x: x is None, [db_fields['lead_id'],db_fields['delayer_db_internal_tag'],db_fields['trigger_date'],db_fields['delayer_db_internal_comment'] ])):
            raise Exception("Lead id, delayer_db_internal_tag,delayer_db_internal_comment and trigger date parameters cannot be empty")

        table_names = [key for key in db_fields.keys() if db_fields[key] is not None]
        values = [db_fields[key] for key in db_fields.keys() if db_fields[key] is not None]
        values_placeholders = ",".join(["%s" for i in values])
        self.cursor.execute(
            f'''
            INSERT INTO DELAYER ({",".join(table_names)})
            VALUES 
            ({values_placeholders})
            ''',values)
        self.connection.commit()

    def create_delayer_table(self):
        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS DELAYER
                (delayer_db_internal_comment     TEXT        NOT NULL,  
                lead_id                        VARCHAR(20)   NOT NULL,  
                delayer_db_internal_tag        VARCHAR(250)  NOT NULL,
                trigger_date                   TIMESTAMP     NOT NULL,
                additional_info                TEXT,
                ID                SERIAL     PRIMARY KEY      NOT NULL
                );
            ''')
        self.connection.commit()

    def delete_record(self,lead_id,internal_tag):
        self.cursor.execute(
            '''
            DELETE FROM delayer WHERE lead_id = %s AND delayer_db_internal_tag = %s;
            ''', [lead_id,internal_tag])
        self.connection.commit()

    def update_record(self, lead_id, internal_tag, trigger_date): 
        self.cursor.execute(
            f'''
            UPDATE delayer SET
                trigger_date = %s
             WHERE lead_id = %s AND delayer_db_internal_tag = %s;
            ''', [trigger_date, lead_id, internal_tag])
        self.connection.commit()