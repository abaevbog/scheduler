import psycopg2
import os 
import pytz
from datetime import datetime
from random import randint
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
    def create_table(self):
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
                COMMENT         TEXT        NOT NULL
                );
            ''')

    #
    def add_new_record(self,**kwargs):
        db_fields = {
            'LEAD_ID': None,
            'LEAD_STATUS':None,
            'NEXT_ACTION':None,
            'EVENT_DATE':None,
            'CUTOFF':None,
            'TYPE':None,
            'FREQUENCY_IN_DAYS_BEFORE_CUTOFF':None,
            'FREQUENCY_IN_DAYS_AFTER_CUTOFF': None
            }
        for key in db_fields.keys():
            if key in **kwargs:
                db_fields[key] = **kwargs[key]                   
        if any(map(lambda x: x is None, [db_fields['LEAD_ID'],db_fields['LEAD_STATUS'],db_fields['NEXT_ACTION']])):
            raise Exception("Lead id, lead status and next action parameters cannot be empty")

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


    def fetch_reminders(self):
        tz = pytz.timezone('America/New_York')
        now = datetime.now(tz)
        now_pretty = now.strftime("%Y-%m-%d %H:%M:%S")
        recs = self.cursor.execute(
            f'''
            SELECT * FROM SCHEDULER WHERE next_action <= {now_pretty}::timestamp
            '''
        )
        return recs

    def delete_record(self):
        return 1

    def update_next_dates_of_reminders(self):
        return 1
