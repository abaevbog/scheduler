import psycopg2
import os 
import pytz
from datetime import datetime
from random import randint
from salesforce import Salesforce


#make sure you don't forget to close connection
class Database():
    def __init__(self):
        conn = psycopg2.connect(
            database = os.environ['DB_NAME'],
            user = os.environ['DB_USER'], 
            password = os.environ['DB_PASSWORD'], 
            host = os.environ['DB_HOST'], 
            port = os.environ['DB_PORT']
        )
        self.connection = conn
        self.cursor = conn.cursor()

    # This will go into terraform ... or something.
    # Should be run when DB is created
    # Creates the main table where all info lives
    
    def create_main_table(self):
        self.cursor.execute(
            '''
            CREATE TABLE    SCHEDULER
                (ID   INT     PRIMARY KEY         NOT NULL,  
                lead_id       VARCHAR(20)        NOT NULL,  
                lead_status    VARCHAR(250)       NOT NULL,
                next_action    TIMESTAMP          NOT NULL,
                url_to_hit     TEXT               NOT NULL,
                event_date     TIMESTAMP,
                cutoff         TIMESTAMP,
                type           VARCHAR(250),
                frequency_in_days_before_cutoff INT,
                frequency_in_days_after_cutoff INT,
                required_salesforce_fields   VARCHAR(250)[],
                comment         TEXT        NOT NULL
                );
            CREATE EXTENSION aws_s3 CASCADE;
            ''')
    
    # Create table where we'll put data with boolean fields 
    # fetched from salesforce for a join after.
    def create_SALESFORCE_RECORDS_table(self, boolean_fields):
        db_rows = [f"{field.upper()} BOOLEAN," for field in boolean_fields]
        db_rows = db_rows[:-1]
        self.cursor.execute(
            f'''
            CREATE TABLE SALESFORCE_RECORDS 
            (lead_id    VARCHAR(20)  PRIMARY KEY  NOT NULL,
            {db_rows}
            );
            '''
        )

    def add_new_record(self,**kwargs):
        db_fields = {
            'LEAD_ID': None,
            'lead_status':None,
            'next_action':None,
            'event_date':None,
            'cutoff':None,
            'type':None,
            'frequency_in_days_before_cutoff':None,
            'frequency_in_days_after_cutoff': None,
            'required_salesforce_fields' : None,
            'comment' : None
            }
        for key in db_fields.keys():
            if key in **kwargs:
                db_fields[key] = **kwargs[key]                   
        if any(map(lambda x: x is None, [db_fields['LEAD_ID'],db_fields['lead_status'],db_fields['next_action'],db_fields['comment'] ])):
            raise Exception("Lead id, lead status,comment and next action parameters cannot be empty")

        uid = randint(0,1000000)
        table_names = [key for key in db_fields.keys() if db_fields[key] is not None]
        values = [db_fields[key] for key in db_fields.keys() if db_fields[key] is not None]
        self.cursor.execute(
            f'''
            INSERT INTO SCHEDULER ({",".join(table_names)})
            VALUES 
            ({",".join(values)})
            '''
        )

    # fetch actions that need to happen right now
    def fetch_due_actions(self):
        tz = pytz.timezone('America/New_York')
        now = datetime.now(tz)
        now_pretty = now.strftime("%Y-%m-%d %H:%M:%S")
        recs = self.cursor.execute(
            f'''
            SELECT * FROM SCHEDULER WHERE next_action <= {now_pretty}::timestamp
            '''
        )
        return self.cursor.fetchall()

    def delete_records(self, lead_ids):      
        self.cursor.execute(
            f'''
            DELETE FROM SCHEDULER WHERE lead_id IN {lead_ids}
            '''
        )

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
            '''
        )

    # delete records that do not have CUTOFF value (meaning, 
    # ones that require only one action)
    def delete_expired_one_time_records(self):
        tz = pytz.timezone('America/New_York')
        now = datetime.now(tz)
        now_pretty = now.strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute(
            f'''
            DELETE FROM SCHEDULER  WHERE next_action <= {now_pretty}::timestamp AND cutoff IS NULL;
            '''
        )

    #
    def reload_salesforce_records(self, boolean_fields):
        self.cursor.execute("DROP TABLE SALESFORCE_RECORDS;")
        self.create_SALESFORCE_RECORDS_table(boolean_fields)

    # load data from s3 into SALESFORCE_RECORDS table
    def export_data_from_s3(self):
        bucket = os.getenv["BUCKET"]
        self.cursor.execute(
            f'''
            SELECT aws_s3.table_import_from_s3(
            'SALESFORCE_RECORDS',
            '',
            'DELIMITER "\t"', 
            aws_commons.create_s3_uri('{bucket}', 'scheduler/records.csv', 'us-east-1')
            );'''
        )
        
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

    # fetch all actions, check with salesforce
    # for all records that have all prerequisites satisfied
    # delete them. Probably adjust salesforce module
    def expire_satisfied_records(self):
        s = Salesforce()
        s.authenticate()
        # get all up to date boolean fields from salesforce
        boolean_fields, date_fields = s.get_object_fields()
        # get all lead ids from db
        all_lead_ids = self.fetch_all_lead_ids()
        # fetch records with given lead ids and write them to s3
        s.write_records_to_s3(all_lead_ids,boolean_fields)
        # toss away old status table and load new data into it
        self.reload_salesforce_records()
        self.export_data_from_s3()
        # then, for every type of notification (text, email, other)
        # we want to perform a join with scheduler and status table
        # to get table like: lead_idFIELDS_REQUIRED FIELD_ONE(true/false) FIELD_TWO(true/false)
        old_entries = self.find_satisfied_records()
        self.delete_records(old_entries)
