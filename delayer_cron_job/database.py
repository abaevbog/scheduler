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
        self.now_rounded = datetime.now(pytz.timezone('America/New_York')).replace(minute=0).strftime("%Y-%m-%d %H:%M")
        self.connection.autocommit = True

    # fetch actions that need to happen right now
    def fetch_due_actions(self):
        recs = self.cursor.execute(
            f'''
            SELECT * FROM DELAYER WHERE trigger_date <= %s::timestamp AND NOT on_hold;
            ''',[self.now_rounded])
        return self.cursor.fetchall()

    # fetch actions that need to happen right now
    def fetch_all_lead_ids(self):
        self.cursor.execute("SELECT lead_id FROM delayer;")
        return [row[0] for row in self.cursor.fetchall()]

    # delete records that are expired
    def delete_expired_records(self):
        self.cursor.execute(
            f'''
            DELETE FROM DELAYER  WHERE trigger_date <= %s::timestamp RETURNING *;
            ''',[self.now_rounded])
        deleted = self.cursor.fetchall()
        for d in deleted:
            self.print_record("DELAYER DATABASE EXPIRED",d)


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


    def insert_salesforce_data(self, data):
        print("Inserting",data)
        for dic in data:
            precon = dic['PRECON_DATE__c']
            predemo = dic['PREDEMO_DATE__c']
            lead = dic['Id']
            on_hold = dic['ON_HOLD__c']
            self.cursor.execute(
                f'''
                UPDATE delayer
                SET precon_or_predemo_date = %s::timestamp
                WHERE lead_id = %s AND wait_for_precon_or_predemo = 'PRECON'
                RETURNING *;
                ''',[precon, lead])
            updated = self.cursor.fetchall()
            for d in updated:
                self.print_record("DELAYER INSERTED",d)
            self.cursor.execute(
                f'''
                UPDATE delayer
                SET precon_or_predemo_date = %s::timestamp
                WHERE lead_id = %s AND wait_for_precon_or_predemo = 'PREDEMO'
                RETURNING *;
                ''',[predemo, lead])
            updated = self.cursor.fetchall()
            for d in updated:
                self.print_record("DELAYER INSERTED",d)
            self.cursor.execute(
                f'''
                UPDATE delayer
                SET on_hold = %s
                WHERE lead_id = %s
                RETURNING *;
                ''', [on_hold, predemo])
            updated = self.cursor.fetchall()
            for d in updated:
                self.print_record("DELAYER INSERTED",d)


    def update_start_date_depending_on_precon(self):
        self.cursor.execute(
            f'''
            UPDATE delayer
            SET trigger_date = precon_or_predemo_date::timestamp - days_before_precon_or_predemo * interval '1 day'
            WHERE precon_or_predemo_date is not NULL AND trigger_date != precon_or_predemo_date::timestamp - days_before_precon_or_predemo * interval '1 day'
            RETURNING *;
            ''', [self.now_rounded, self.now_rounded ])
        updated = self.cursor.fetchall()
        for d in updated:
            self.print_record("DELAYER DATABASE UPDATED BASED ON PRECON/PREDEMO",d)


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


    def add_new_record(self,**kwargs):
        db_fields = {
                'delayer_db_internal_tag':None,
                'lead_id':None,
                'delayer_db_internal_comment':None,
                'trigger_date':None,
                'additional_info':None,
                'wait_for_precon_or_predemo':None,
                'days_before_precon_or_predemo':None,
                'precon_or_predemo':None,
                'precon_or_predemo_date':None
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