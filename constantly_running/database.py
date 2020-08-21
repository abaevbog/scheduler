import psycopg2
import os 
import pytz
import sys
from datetime import datetime
from random import randint
import psycopg2.extras
from psycopg2.errors import UniqueViolation
from send_to_cloudwatch import Log
class Database():
    def __init__(self, config):
        self.conn = psycopg2.connect(
            database = config.get('database'),
            user = config.get('user'), 
            password = config.get('password'), 
            host = config.get('host'), 
            port = config.get('port')
        )
        self.conn.autocommit = True 
        self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        self.config = config
        self.log = Log()


    def get_fields(self, operator):
        self.cursor.execute(f'''
            select column_name 
            from information_schema.columns 
            where table_name = '{operator}'; 
        ''')
        fields = [row[0] for row in self.cursor.fetchall()]
        return  fields


    def add_record(self,db_fields, operator): 
        table_names = [key for key in db_fields.keys() ]
        values = [db_fields[key] for key in db_fields.keys() ]
        values_placeholders = ",".join(["%s" for i in values])
        try:
            self.cursor.execute(
                f'''
                INSERT INTO {operator} ({",".join(table_names)})
                VALUES 
                ({values_placeholders})
                RETURNING *;
                ''',values)
        except UniqueViolation as e:
            print(e)


    def delete_record(self,operator, lead_id,tag):
        self.cursor.execute(
            f'''
            DELETE FROM {operator} WHERE lead_id = %s AND tag = %s
            RETURNING *;
            ''', [lead_id,tag])

    def update_record(self,operator,lead_id,tag, field_name, new_value):
        self.cursor.execute(
            f'''
            UPDATE {operator}
            SET {field_name} = {new_value}
            WHERE lead_id = %s AND tag = %s
            RETURNING *;
            ''', [lead_id,tag])


    def print_record(self,operator, prefix, record):
        log = ""
        for key in record:
            field_value = record[key]
            if isinstance(field_value , datetime):
                log+=f"{key}: {field_value.strftime('%Y-%m-%d %H:%M')} -- "
            else:
                log += f"{key}: {field_value} -- "
        self.log.send_to_cloudwatch(operator,f"{prefix} | {log}\n--------------") 