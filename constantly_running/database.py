import boto3
import requests
import psycopg2
import os 
import pytz
from datetime import datetime
from random import randint

class Database():
    def __init__(self, config):
        print("Initing DB")
        print(config)
        conn = psycopg2.connect(
            database = config.get('database'),
            user = config.get('user'), 
            password = config.get('password'), 
            host = config.get('host'), 
            port = config.get('port')
        )
        self.connection = conn
        self.cursor = conn.cursor()
        self.config = config
        print("DN connected")


    def delete_record(self, lead_id):      
        self.cursor.execute(
            f'''
            DELETE FROM SCHEDULER WHERE lead_id = %s;
            ''', [lead_id])
        self.connection.commit()

    def get_fields(self):
        print("Getting fields")
        return  [
                'lead_id',
                'lead_status',
                'next_action',
                'event_date',
                'cutoff',
                'type',
                'url_to_hit',
                'frequency_in_days_before_cutoff',
                'frequency_in_days_after_cutoff',
                'required_salesforce_fields' ,
                'comment' 
            ]

    def add_new_record(self,**kwargs):
        db_fields = {
            'lead_id': None,
            'lead_status':None,
            'next_action':None,
            'event_date':None,
            'cutoff':None,
            'type':None,
            'url_to_hit':None,
            'frequency_in_days_before_cutoff':None,
            'frequency_in_days_after_cutoff': None,
            'required_salesforce_fields' : None,
            'comment' : None
            }
        for key in db_fields.keys():
            if key in dict(kwargs.items()):
                db_fields[key] = dict(kwargs.items())[key]                   
        if any(map(lambda x: x is None, [db_fields['lead_id'],db_fields['lead_status'],db_fields['next_action'],db_fields['comment'] ])):
            raise Exception("Lead id, lead status,comment and next action parameters cannot be empty")

        uid = randint(0,1000000)
        table_names = ['id'] + [key for key in db_fields.keys() if db_fields[key] is not None]
        values = [uid] + [db_fields[key] for key in db_fields.keys() if db_fields[key] is not None]
        values_placeholders = ",".join(["%s" for i in values])
        self.cursor.execute(
            f'''
            INSERT INTO SCHEDULER ({",".join(table_names)})
            VALUES 
            ({values_placeholders})
            ''',values)
        self.connection.commit()

        
    def create_main_table(self):
        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS SCHEDULER
                (ID   INT     PRIMARY KEY         NOT NULL,  
                lead_id       VARCHAR(20)        NOT NULL,  
                lead_status    VARCHAR(250)       NOT NULL,
                next_action    TIMESTAMP          NOT NULL,
                url_to_hit     TEXT ,
                event_date     TIMESTAMP,
                cutoff         TIMESTAMP,
                type           VARCHAR(250),
                frequency_in_days_before_cutoff INT,
                frequency_in_days_after_cutoff INT,
                required_salesforce_fields   VARCHAR(250)[],
                comment         TEXT        NOT NULL
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
              not_satisfied TEXT[]
            );
            ''')
        self.connection.commit()