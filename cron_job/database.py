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
            SELECT * FROM SCHEDULER WHERE next_action <= %s::timestamp AND %s::timestamp <= event_date
            ''',[now_pretty, now_pretty])
        return self.cursor.fetchall()

    def delete_records(self, lead_ids):      
        self.cursor.execute(
            f'''
            DELETE FROM SCHEDULER WHERE id = Any(%s);
            ''', [lead_ids])
        self.connection.commit()

    # update date of when the action should be triggered next time
    def update_next_dates_of_due_actions(self):
        tz = pytz.timezone('America/New_York')
        now = datetime.now(tz)
        now_pretty = now.strftime("%Y-%m-%d %H:%M")
        self.cursor.execute(
            f'''
            UPDATE SCHEDULER
            SET next_action= scheduler.next_action + due.frequency_in_days_before_cutoff * interval '1 day'
            FROM (SELECT * FROM SCHEDULER
                WHERE next_action <= %s::timestamp AND cutoff IS NOT NULL) AS due
            WHERE scheduler.next_action < scheduler.cutoff RETURNING SCHEDULER.id;
            ''', [now_pretty])
        updated_ids = [row[0] for row in self.cursor.fetchall()]
        self.cursor.execute( '''
            UPDATE SCHEDULER
            SET next_action= scheduler.next_action + due.frequency_in_days_after_cutoff * interval '1 day'
            FROM (SELECT * FROM SCHEDULER
                WHERE next_action <= %s::timestamp AND cutoff IS NOT NULL ) AS due
            WHERE scheduler.next_action >= scheduler.cutoff AND NOT( scheduler.id = ANY(%s) );
            ''',[now_pretty,updated_ids])
        self.connection.commit()

    # delete records that do not have CUTOFF value (meaning, 
    # ones that require only one action)
    def delete_expired_one_time_records(self):
        tz = pytz.timezone('America/New_York')
        now = datetime.now(tz)
        now_pretty = now.strftime("%Y-%m-%d %H:%M")
        self.cursor.execute(
            f'''
            DELETE FROM SCHEDULER  WHERE (next_action <= %s::timestamp AND cutoff IS NULL) OR (event_date <= %s::timestamp );
            ''',[now_pretty, now_pretty])
        self.connection.commit()

    #
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
            SELECT * FROM (SELECT * FROM SCHEDULER sch INNER JOIN SALESFORCE_RECORDS sr
            ON sch.lead_id= sr.id ) as joined where 
            (joined.required_salesforce_fields IS NOT NULL AND joined.required_salesforce_fields::text[] <@ joined.satisfied)
            OR (joined.status = 'SALE CANCELLED') OR (ARRAY['on_hold__c'] <@ joined.satisfied );
            '''
        )
        return [row[0] for row in self.cursor.fetchall()]

    # get literally all lead ids from db
    def fetch_all_lead_ids(self):
        self.cursor.execute("SELECT lead_id FROM SCHEDULER;")
        return [row[0] for row in self.cursor.fetchall()]


