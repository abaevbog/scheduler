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
                LEAD_ID        VARCHAR(20)        NOT NULL,  
                LEAD_STATUS    VARCHAR(250)       NOT NULL,
                NEXT_ACTION    TIMESTAMP          NOT NULL,
                EVENT_DATE     TIMESTAMP,
                CUTOFF         TIMESTAMP,
                TYPE           VARCHAR(250),
                FREQUENCY_IN_DAYS_BEFORE_CUTOFF INT,
                FREQUENCY_IN_DAYS_AFTER_CUTOFF INT,
                REQUIRED_SALESFORCE_FIELDS   VARCHAR(250)[],
                COMMENT         TEXT        NOT NULL
                );
            CREATE EXTENSION aws_s3 CASCADE;
            ''')
    
    # Create table where we'll put data with boolean fields 
    # fetched from salesforce for a join after.
    def create_leads_status_table(self, boolean_fields):
        db_rows = [f"{field.upper()} BOOLEAN," for field in boolean_fields]
        db_rows = db_rows[:-1]
        self.cursor.execute(
            f'''
            CREATE TABLE LEADS_STATUS 
            (LEAD_ID     VARCHAR(20)  PRIMARY KEY  NOT NULL,
            {db_rows}
            );
            '''
        )

    def add_new_record(self,**kwargs):
        db_fields = {
            'LEAD_ID': None,
            'LEAD_STATUS':None,
            'NEXT_ACTION':None,
            'EVENT_DATE':None,
            'CUTOFF':None,
            'TYPE':None,
            'FREQUENCY_IN_DAYS_BEFORE_CUTOFF':None,
            'FREQUENCY_IN_DAYS_AFTER_CUTOFF': None,
            'REQUIRED_SALESFORCE_FIELDS' : None,
            'COMMENT' : None
            }
        for key in db_fields.keys():
            if key in **kwargs:
                db_fields[key] = **kwargs[key]                   
        if any(map(lambda x: x is None, [db_fields['LEAD_ID'],db_fields['LEAD_STATUS'],db_fields['NEXT_ACTION'],db_fields['COMMENT'] ])):
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


    def fetch_due_reminders(self):
        tz = pytz.timezone('America/New_York')
        now = datetime.now(tz)
        now_pretty = now.strftime("%Y-%m-%d %H:%M:%S")
        recs = self.cursor.execute(
            f'''
            SELECT * FROM SCHEDULER WHERE next_action <= {now_pretty}::timestamp
            '''
        )
        return recs

    def delete_records(self, lead_id):
        if len(lead_id) != 15:
            raise Exception("Invalid lead id: salesforce lead id is 15 characters.")
        self.cursor.execute(
            f'''
            DELETE FROM SCHEDULER WHERE LEAD_ID = {lead_id}
            '''
        )

    def update_next_dates_of_reminders(self):
        return 1

    def reload_status_table(self, boolean_fields):
        self.cursor.execute("DROP TABLE LEADS_STATUS;")
        self.create_leads_status_table(boolean_fields)


    def export_data_from_s3(self):
        bucket = os.getenv["BUCKET"]
        self.cursor.execute(
            f'''
            SELECT aws_s3.table_import_from_s3(
            'LEADS_STATUS',
            '',
            'DELIMITER "\t"', 
            aws_commons.create_s3_uri('{bucket}', 'scheduler/records.csv', 'us-east-1')
            );'''
        

    # fetch all reminders, check with salesforce
    # for all records that have all prerequisites satisfied
    # delete them. Probably adjust salesforce module
    def expire_satisfied_records(self):
        s = Salesforce()
        s.authenticate()
        # get all up to date boolean fields from salesforce
        boolean_fields, date_fields = s.get_object_fields()
        # get all lead ids from db
        self.cursor.execute("SELECT LEAD_ID FROM SCHEDULER;")
        all_lead_ids = [row[0] for row in self.cursor.fetchall()]
        # fetch records with given lead ids and write them to s3
        s.write_records_to_s3(all_lead_ids,boolean_fields)
        # toss away old status table and load new data into it
        self.reload_status_table()
        self.export_data_from_s3()
        # then, for every type of notification (text, email, other)
        # we want to perform a join with scheduler and status table
        # to get table like: LEAD_ID FIELDS_REQUIRED FIELD_ONE(true/false) FIELD_TWO(true/false)
