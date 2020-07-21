import psycopg2
import os 
import pytz
import sys
from datetime import datetime
from random import randint

class Scheduler():
    def __init__(self,conn,cursor):
        self.connection = conn
        self.cursor = cursor 
        self.db_fields = {
            'reminders_db_internal_comment' : None,
            'lead_id': None,
            'reminders_db_internal_tag':None,
            'next_action':None,
            'event_date':None,
            'cutoff':None,
            'type':None,
            'frequency_in_days_before_cutoff':None,
            'frequency_in_days_after_cutoff': None,
            'required_salesforce_fields' : None
        }
    def create_reminders_table(self):
        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS SCHEDULER
                (reminders_db_internal_comment         TEXT        NOT NULL,  
                lead_id       VARCHAR(20)        NOT NULL,  
                reminders_db_internal_tag    VARCHAR(250)       NOT NULL,
                next_action    TIMESTAMP          NOT NULL,
                event_date     TIMESTAMP,
                cutoff         TIMESTAMP,
                type           VARCHAR(250),
                frequency_in_days_before_cutoff INT,
                frequency_in_days_after_cutoff INT,
                required_salesforce_fields   VARCHAR(250)[],
                ID   SERIAL     PRIMARY KEY      NOT NULL
                );
            ''')
        self.connection.commit()

    def create_salesforce_recs_table(self):
        self.cursor.execute(
            f'''
            CREATE TABLE IF NOT EXISTS SALESFORCE_RECORDS 
            ( Id  VARCHAR(20)  PRIMARY KEY  NOT NULL,
              NAME VARCHAR(100) NOT NULL,
              satisfied TEXT[],
              not_satisfied TEXT[],
              status VARCHAR(30)
            );
            ''')
        self.connection.commit()

    def add_record(self,**kwargs):
        db_fields = self.db_fields.copy()
        for key in db_fields.keys():
            if key in dict(kwargs.items()):
                db_fields[key] = dict(kwargs.items())[key]                   
        if any(map(lambda x: x is None, [db_fields['lead_id'],db_fields['reminders_db_internal_tag'],db_fields['next_action'],db_fields['reminders_db_internal_comment'] ])):
            raise Exception("Lead id, reminders_db_internal_tag,reminders_db_internal_comment and next action parameters cannot be empty")

        table_names = [key for key in db_fields.keys() if db_fields[key] is not None]
        values = [db_fields[key] for key in db_fields.keys() if db_fields[key] is not None]
        values_placeholders = ",".join(["%s" for i in values])
        self.cursor.execute(
            f'''
            INSERT INTO SCHEDULER ({",".join(table_names)})
            VALUES 
            ({values_placeholders})
            ''',values)
        self.connection.commit()

    def get_fields(self):
        return  list(self.db_fields.keys())

    def update_record(self, lead_id, new_cutoff, new_event_date, new_next_action=None): 
        set_next_action = "" 
        inputs = [new_cutoff,new_event_date,lead_id]
        if new_next_action is not None:
            set_next_action = ",next_action = %s"
            inputs = [new_cutoff,new_event_date,new_next_action,lead_id]
        self.cursor.execute(
            f'''
            UPDATE SCHEDULER SET
                cutoff = %s,
                event_date = %s
                {set_next_action}
             WHERE lead_id = %s;
            ''', inputs)
        self.connection.commit()

    def delete_record(self,lead_id,internal_tag):
        self.cursor.execute(
            '''
            DELETE FROM scheduler WHERE lead_id = %s AND delayer_db_internal_tag = %s;
            ''', [lead_id,internal_tag])
        self.connection.commit()


    def print_record(self, prefix, record):
        fields = [
                'reminders_db_internal_tag',
                'lead_id',
                'reminders_db_internal_comment',
                'next_action',
                'event_date',
                'cutoff',
                'type',
                'frequency_in_days_before_cutoff',
                'frequency_in_days_after_cutoff',
                'required_salesforce_fields' ,
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