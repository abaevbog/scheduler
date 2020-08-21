import sys
sys.path.append('/Users/bogdanabaev/RandomProgramming/BasementRemodeling/scheduler/scheduler/delayer')
sys.path.append('/Users/bogdanabaev/RandomProgramming/BasementRemodeling/scheduler/scheduler/')
from salesforce import Salesforce
import unittest
from delayer import Delayer
import boto3
import configparser
from entries import Dummy
import pytz
from datetime import datetime, timedelta
from psycopg2.errors import UniqueViolation
      
config = configparser.ConfigParser()
with open(r'scheduler.conf') as f:
    config.read_file(f)
salesforce = Salesforce(config)
database = Delayer(config)
token = salesforce.authenticate()

class Testing(unittest.TestCase):

    def test_aaaaaa_db_setup(self):
        #print("DB SETUP")
        dummy = Dummy()
        database.cursor.execute(
            '''
            Truncate delayer_v2;
            Truncate salesforce_recs;
            '''
        )
        database.add_salesforce_records(dummy.salesforce_entries,["id","name", "satisfied", "not_satisfied","status", "START_DATE"])
        for entry in dummy.database_entries:
            database.add_new_record(entry)
            try:
                database.add_new_record(entry)
            except UniqueViolation as e:
                print(e)


    def test_bbbbbb_sync_salesforce(self):
        #print("SYNCING DUE DATES")
        database.sync_start_dates_w_salesforce()
        database.cursor.execute('''
            SELECT * FROM delayer_v2;
        ''')
        entries = database.cursor.fetchall()

        

    def test_ccccc_get_due_actions(self):
        #print("DUE ACTIONS")
        due = database.fetch_due_actions()
        print("DUE: ", due)

    def test_dddddddd_delete_expired_recs(self):
        #print("DELETE EXPIRED")
        database.delete_expired_records()
        



if __name__ == '__main__': 
    unittest.main() 