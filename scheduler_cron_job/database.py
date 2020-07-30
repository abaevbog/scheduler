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
            SELECT * FROM SCHEDULER WHERE NOT on_hold AND 
            (next_action <= %s::timestamp AND %s::timestamp <= event_date)
            OR  (next_action <= %s::timestamp AND event_date is NULL);
            ''',[now_pretty, now_pretty])
        return self.cursor.fetchall()

    def delete_records(self, lead_ids):   
        self.cursor.execute(
            f'''
            DELETE FROM SCHEDULER WHERE id = Any(%s) RETURNING *;
            ''', [lead_ids])
        deleted = self.cursor.fetchall()
        self.connection.commit()
        return deleted 

    # update date of when the action should be triggered next time
    def update_next_dates_of_due_actions(self):
        tz = pytz.timezone('America/New_York')
        now = datetime.now(tz)
        now_pretty = now.strftime("%Y-%m-%d %H:%M")
        self.cursor.execute(
            f'''
            UPDATE SCHEDULER
            SET next_action= %s::timestamp + due.frequency_in_days_before_cutoff * interval '1 day'
            FROM (SELECT * FROM SCHEDULER
                WHERE next_action <= %s::timestamp) AS due
            WHERE scheduler.next_action < scheduler.cutoff RETURNING SCHEDULER.id;
            ''', [now_pretty,now_pretty])
        updated_ids = [row[0] for row in self.cursor.fetchall()]
        self.cursor.execute('''
            UPDATE SCHEDULER
            SET next_action= %s::timestamp + due.frequency_in_days_after_cutoff * interval '1 day'
            FROM (SELECT * FROM SCHEDULER
                WHERE next_action <= %s::timestamp) AS due
            WHERE scheduler.next_action >= scheduler.cutoff AND NOT( scheduler.id = ANY(%s) );
            ''',[now_pretty,now_pretty,updated_ids])
        self.connection.commit()

    # delete records that reached event date
    def delete_expired_records(self):
        tz = pytz.timezone('America/New_York')
        now = datetime.now(tz)
        now_pretty = now.strftime("%Y-%m-%d %H:%M")
        self.cursor.execute(
            f'''
            DELETE FROM SCHEDULER  WHERE event_date <= %s::timestamp RETURNING *;
            ''',[now_pretty])
        deleted = self.cursor.fetchall()
        for d in deleted:
            self.print_record("SCHEDULER DATABASE EXPIRED",d)
        self.connection.commit()
    
    def truncate_salesforce_records(self):
        self.cursor.execute("TRUNCATE SALESFORCE_RECORDS;")
        self.connection.commit()


    def insert_data_to_salesforce_recs(self, data):
        placeholders = ",".join(["(%s,%s,%s,%s)" for i in data])
        recs_array = []
        for dic in data:
            recs_array.append(dic['id'])
            recs_array.append(dic['name'])
            recs_array.append(dic['satisfied'])
            recs_array.append(dic['not_satisfied'])
        self.cursor.execute(
        f'''
        INSERT INTO salesforce_records (id, name, satisfied, not_satisfied)
        VALUES {placeholders}
        ''', recs_array)
        self.connection.commit()

        
    #  find records that have all necessary checkboxes checked in salesforce
    # or records that are on hold or records that have been cancelled
    def find_satisfied_records(self):
        self.cursor.execute(
            f'''
            SELECT sch.id FROM SCHEDULER sch INNER JOIN SALESFORCE_RECORDS sr
            ON sch.lead_id = sr.id  where 
            (sch.required_salesforce_fields IS NOT NULL AND sch.required_salesforce_fields::text[] <@ sr.satisfied)
            OR (sr.status = 'SALE CANCELLED');
            '''
        )
        return [row[0] for row in self.cursor.fetchall()]

    # get literally all lead ids from db
    def fetch_all_lead_ids(self):
        self.cursor.execute("SELECT lead_id FROM SCHEDULER;")
        return [row[0] for row in self.cursor.fetchall()]


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

## the functions below are used for testing
    def add_new_record(self,**kwargs):
        db_fields = {
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

        
    def create_main_table(self):
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