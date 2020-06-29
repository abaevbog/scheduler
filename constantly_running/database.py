import boto3
import requests
import psycopg2
import os 
import pytz
from datetime import datetime
from random import randint

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


    def delete_record(self, lead_id):      
        self.cursor.execute(
            f'''
            DELETE FROM SCHEDULER WHERE id = %s;
            ''', [lead_id])
        self.connection.commit()

    def get_fields(self):
        return  {
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
                }

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

        
