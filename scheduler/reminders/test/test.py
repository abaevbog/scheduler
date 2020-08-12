import sys
sys.path.append('/Users/bogdanabaev/RandomProgramming/BasementRemodeling/scheduler/scheduler/reminders')
sys.path.append('/Users/bogdanabaev/RandomProgramming/BasementRemodeling/scheduler/scheduler/')
from salesforce import Salesforce
import unittest
from reminders import Reminders
import boto3
import configparser
from entries import Dummy
import pytz
from datetime import datetime, timedelta
      
config = configparser.ConfigParser()
with open(r'scheduler.conf') as f:
    config.read_file(f)
salesforce = Salesforce(config)
database = Reminders(config)
token = salesforce.authenticate()

class Testing(unittest.TestCase):

    def test_aaaaaa_db_setup(self):
        print("DB SETUP")
        dummy = Dummy()
        database.cursor.execute(
            '''
            Truncate delayer;
            Truncate salesforce_recs;
            '''
        )
        database.add_salesforce_records(dummy.salesforce_entries,["id","name", "satisfied", "not_satisfied","status", "START_DATE"])
        for entry in dummy.database_entries:
            database.add_new_record(entry)


    def test_ccccc_sync_salesforce(self):
        print("SYNCING DUE DATES")
        database.sync_start_dates_w_salesforce()

    def test_dddddddd_delete_expired_recs(self):
        print("Delete expired")
        database.delete_expired_records()

    def test_eeeee_delete_satisfied_recs(self):
        print("Delete satisfied")
        database.delete_satisfied_records()

    def test_fffff_get_due_actions(self):
        due = database.fetch_due_actions()
        print(due)

    def test_gggg_update_records_after_trigger(self):
        database.update_records_after_trigger()
        



if __name__ == '__main__': 
    unittest.main() 
