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

    # This will go into terraform ... or something.
    # Should be run when DB is created
    # Creates the main table where all info lives
    
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
            CREATE EXTENSION IF NOT EXISTS aws_commons;
            CREATE EXTENSION  IF NOT EXISTS aws_s3 CASCADE;
            ''')
        self.connection.commit()
    
    # Create table where we'll put data with boolean fields 
    # fetched from salesforce for a join after.
    def create_salesforce_recs_table(self, boolean_fields):
        print(f"bool fields in db: {boolean_fields}")
        boolean_fields.sort()
        db_rows = [f"{field} BOOLEAN" for field in boolean_fields]
        db_rows_to_be_filled = ",".join([f"{field.upper()} BOOLEAN" for field in boolean_fields])
        print(db_rows_to_be_filled)
        self.cursor.execute(
            f'''
            CREATE TABLE SALESFORCE_RECORDS 
            ( Id  VARCHAR(20)  PRIMARY KEY  NOT NULL,
              NAME VARCHAR(100) NOT NULL,
            {db_rows_to_be_filled}
            );
            ''')
        self.connection.commit()

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
        values = [db_fields[key] for key in db_fields.keys() if db_fields[key] is not None]
        values_formatted = [str(uid)] + list(map(lambda x: "\'" + x + "\'" if isinstance(x,str) else str(x) ,values))
        self.cursor.execute(
            f'''
            INSERT INTO SCHEDULER ({",".join(table_names)})
            VALUES 
            ({",".join(values_formatted)})
            ''')
        self.connection.commit()

    # fetch actions that need to happen right now
    def fetch_due_actions(self):
        tz = pytz.timezone('America/New_York')
        now = datetime.now(tz)
        now_pretty = now.strftime("%Y-%m-%d %H:%M:%S")
        recs = self.cursor.execute(
            f'''
            SELECT * FROM SCHEDULER WHERE next_action <= {now_pretty}::timestamp
            ''')
        return self.cursor.fetchall()

    def delete_records(self, lead_ids):      
        self.cursor.execute(
            f'''
            DELETE FROM SCHEDULER WHERE lead_id IN {lead_ids}
            ''')
        self.connection.commit()

    # update date of when the action should be triggered next time
    def update_next_dates_of_due_actions(self):
        tz = pytz.timezone('America/New_York')
        now = datetime.now(tz)
        now_pretty = now.strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute(
            f'''
            UPDATE SCHEDULER
            SET next_action = next_action + INTERVAL due.frequency_in_days_before_cutoff DAY    
            FROM (SELECT * FROM SCHEDULER WHERE next_action <= {now_pretty}::timestamp AND cutoff IS NOT NULL) as due
            WHERE next_action <= cutoff;
            UPDATE SCHEDULER
            SET next_action = next_action + INTERVAL due.frequency_in_days_after_cutoff DAY    
            FROM (SELECT * FROM SCHEDULER WHERE next_action <= {now_pretty}::timestamp AND cutoff IS NOT NULL) as due
            WHERE next_action >= cutoff;
            ''')
        self.connection.commit()

    # delete records that do not have CUTOFF value (meaning, 
    # ones that require only one action)
    def delete_expired_one_time_records(self):
        tz = pytz.timezone('America/New_York')
        now = datetime.now(tz)
        now_pretty = now.strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute(
            f'''
            DELETE FROM SCHEDULER  WHERE next_action <= {now_pretty}::timestamp AND cutoff IS NULL;
            ''')
        self.connection.commit()

    #
    def reload_salesforce_records(self, boolean_fields):
        self.cursor.execute("DROP TABLE SALESFORCE_RECORDS;")
        self.create_SALESFORCE_RECORDS_table(boolean_fields)

    # load data from s3 into SALESFORCE_RECORDS table
    def import_data_from_s3(self):
        print("EXPORTING FROM S3")
        bucket = self.config.get('database',"BUCKET")
        self.cursor.execute(
            f'''
            SELECT aws_s3.table_import_from_s3(
            'SALESFORCE_RECORDS',
            '',
            'DELIMITER \'\'|\'\'', 
            aws_commons.create_s3_uri('{bucket}', 'scheduler/records.csv', 'us-east-1')
            );''')
        self.connection.commit()
        
    # CHECK HOW IT WORKS OUT WITH DIFFERENT typeS
    # Certainly won't work right away
    # ---
    # find set of records S such that for every
    # Entry in S, all necessary fields of Entry in salesforce
    # have been filled in
    def find_satisfied_records(self):
        self.cursor.execute(
            f'''
            SELECT joined.lead_idFROM (SELECT * FROM SCHEDULER sch INNER JOIN SALESFORCE_RECORDS sr
            ON sch.lead_id= sr.lead_idWHERE) as joined 
            WHERE ALL( SELECT joined.required_salesforce_fields FROM joined) ;
            '''
        )
        return [row[0] for row in self.cursor.fetchall()]

    # get literally all lead ids from db
    def fetch_all_lead_ids(self):
        self.cursor.execute("SELECT lead_idFROM SCHEDULER;")
        return [row[0] for row in self.cursor.fetchall()]

