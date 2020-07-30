import psycopg2
import os 
import pytz
from datetime import datetime
from random import randint

#make sure you don't forget to close connection
class Database():
    def __init__(self, config):
        conn = psycopg2.connect(
            database = config.get('database','DB_NAME'),
            user = config.get('database','DB_USER'), 
            password = config.get('database','DB_PASSWORD'), 
            host = config.get('database','DB_HOST'), 
            port = config.get('database','DB_PORT')
        )
        self.connection = conn
        self.cursor = conn.cursor()
        self.config = config

    # fetch actions that need to happen right now
    def fetch_due_actions(self):
        tz = pytz.timezone('America/New_York')
        now = datetime.now(tz)
        now_pretty = str(now.strftime("%Y-%m-%d %H:%M"))
        recs = self.cursor.execute(
            f'''
            SELECT * FROM DELAYER WHERE trigger_date <= %s::timestamp AND NOT on_hold;
            ''',[now_pretty])
        return self.cursor.fetchall()


    # delete records that are expired
    def delete_expired_records(self):
        tz = pytz.timezone('America/New_York')
        now = datetime.now(tz)
        now_pretty = now.strftime("%Y-%m-%d %H:%M")
        self.cursor.execute(
            f'''
            DELETE FROM DELAYER  WHERE trigger_date <= %s::timestamp RETURNING *;
            ''',[now_pretty])
        deleted = self.cursor.fetchall()
        for d in deleted:
            self.print_record("DELAYER DATABASE EXPIRED",d)
        self.connection.commit()



    def print_record(self, prefix, record):
        fields = [
                'delayer_db_internal_tag',
                'lead_id',
                'delayer_db_internal_comment',
                'trigger_date',
                'additional_info',
                'id'
            ]
        log = ""
        for num,name in enumerate(fields):
            field_value = record[num]
            if isinstance(field_value , datetime):
                log+=f"{name}: {record[num].strftime('%Y-%m-%d %H:%M')} -- "
            else:
                log += f"{name}: {record[num]} -- "
        print(f"{prefix} | {log}")
        print("--------------")


### FOR TESTING:

    def create_delays_table(self):
        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS DELAYER
                (delayer_db_internal_comment     TEXT        NOT NULL,  
                lead_id                        VARCHAR(20)   NOT NULL,  
                delayer_db_internal_tag        VARCHAR(250)  NOT NULL,
                trigger_date                   TIMESTAMP     NOT NULL,
                additional_info                TEXT,
                id                SERIAL     PRIMARY KEY      NOT NULL
                );
            ''')
        self.connection.commit()


    def add_new_record(self,**kwargs):
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