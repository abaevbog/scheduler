import sys
sys.path.append('/Users/bogdanabaev/RandomProgramming/BasementRemodeling/scheduler/delayer_cron_job/')
import unittest
from database import Database
from salesforce import Salesforce
import configparser
from entries import Dummy
from datetime import datetime, timedelta
      
config = configparser.ConfigParser()
with open(r'scheduler.conf') as f:
    config.read_file(f)
salesforce = Salesforce(config)
salesforce.authenticate()
database = Database(config)

class Testing(unittest.TestCase):

    def test_aaaaaa_db_setup(self):
        print("DB SETUP")
        database.create_delays_table() 
        database.cursor.execute('''
            TRUNCATE SALESFORCE_RECORDS;
            truncate scheduler;
            truncate delayer;       
        ''')
        dummy = Dummy()
        database.add_new_record(**dummy.param_one)
        database.add_new_record(**dummy.param_two)
        database.add_new_record(**dummy.param_three) 
        database.add_new_record(**dummy.param_four)    


    def test_bbbbbbb_renew_predemo_dates(self):
        print("RENEW PRECON_DATES")
        all_lead_ids = database.fetch_all_lead_ids()
        recs = salesforce.get_records(all_lead_ids)
        print(recs)
        database.insert_salesforce_data(recs)
        database.update_start_date_depending_on_precon()
        database.cursor.execute("select * from delayer where delayer_db_internal_comment='Precon date TO BE UPDATED'")
        x = database.cursor.fetchall()
        print(x)
        self.assertTrue(x[0][3].day == 13)

    def test_ccccc_delete_due_recs(self):
        print("DELETE OLD RECORDS")
        due = database.fetch_due_actions()
        self.assertEqual(due[0][0], 'Due')
        database.delete_expired_records()
        database.cursor.execute("select * from delayer where delayer_db_internal_comment='Due'")
        self.assertTrue(database.cursor.fetchall() == [])


    def test_dddddd_ensure_new(self):
        print("ENSURE NOT DUE IS THERE")
        database.cursor.execute("select * from delayer where delayer_db_internal_comment='Not due'")
        res = database.cursor.fetchall()
        self.assertTrue(len(res) > 0)


if __name__ == '__main__': 
    unittest.main() 
