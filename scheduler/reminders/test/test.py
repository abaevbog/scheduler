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
dummy = Dummy()


class Testing(unittest.TestCase):

    def test_aaaaaa_db_setup(self):
        print("DB SETUP")
        database.cursor.execute(
            '''
            Truncate reminder;
            Truncate salesforce_recs;
            '''
        )
        database.add_salesforce_records(dummy.salesforce_entries,["id","name", "satisfied", "not_satisfied","status", "START_DATE"])
        for entry in dummy.database_entries:
            database.add_new_record(entry)


    def test_ccccc_sync_salesforce(self):
        print("SYNCING DUE DATES")
        synced = database.sync_start_dates_w_salesforce()
        ids = [x[7] for x in synced]
        ids.sort()
        self.assertEqual(ids , [6,7])
        for entry in synced:
            trigger_date_def = entry['trigger_date_definition'].replace('(','').replace(')','').split(',')
            days_before_start = int(trigger_date_def[0])
            start_date_sf = list(filter(lambda x:x['id'] == entry['lead_id'] ,dummy.salesforce_entries))[0]['START_DATE']
            date_object_sf = datetime.strptime(start_date_sf, '%Y-%m-%d %H:%M:%S').date()
            next_action_expected = date_object_sf - timedelta(days=days_before_start)
            self.assertEqual(datetime.strptime(trigger_date_def[1].replace("\"",''), '%Y-%m-%d %H:%M:%S').date(),next_action_expected  )


    def test_dddddddd_delete_expired_recs(self):
        print("Delete expired")
        deleted = database.delete_expired_records()
        ids = [int(x['id']) for x in deleted]
        ids.sort()
        self.assertEqual(ids,[3,7])

    def test_eeeee_delete_satisfied_recs(self):
        print("Delete satisfied")
        deleted = database.delete_satisfied_records()
        ids = [x['id'] for x in deleted]
        ids.sort()
        self.assertEqual(ids,[4,8])

    def test_fffff_get_due_actions(self):
        due = database.fetch_due_actions()
        ids = [x[7] for x in due]
        ids.sort()
        self.assertEqual(ids,[2,6])
      
    def test_gggg_update_records_after_trigger(self):
        
        updated = database.update_records_after_trigger()
        ids = [x[7] for x in updated]
        ids.sort()
        self.assertEqual(ids,[2,6])
        for u in updated:
            entry_id = u[7]
            trigger_date_def = u['trigger_date_definition'].replace('(','').replace(')','').split(',')
            cutoff = u['cutoff'].replace('(','').replace(')','').split(',')
            days_before, before, after =  cutoff[0], cutoff[1], cutoff[2]
            original_next_date = list(filter(lambda x: x['id'] == int(u[0]) ,dummy.database_entries))[0]['trigger_date_definition'][1]
            original_next_date_obj = datetime.strptime(original_next_date, '%Y-%m-%d %H:%M:%S').date()
            my_next_date = datetime.strptime(trigger_date_def[1].replace("\"",''), '%Y-%m-%d %H:%M:%S').date()
            lead_start_date = list(filter(lambda x: int(x['id']) == int(u['lead_id']) ,dummy.salesforce_entries))[0]['START_DATE']
            lead_start_date_obj = datetime.strptime(lead_start_date, '%Y-%m-%d %H:%M:%S').date()
            if datetime.now().date() < lead_start_date_obj - timedelta(days=int(days_before) ):
                self.assertEqual(my_next_date,original_next_date_obj + timedelta(days=int(before)) )
            else:
                self.assertEqual(my_next_date,original_next_date_obj + timedelta(days=int(after)) )

if __name__ == '__main__': 
    unittest.main() 
