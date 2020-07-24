import sys
sys.path.append('/Users/bogdanabaev/RandomProgramming/BasementRemodeling/scheduler/delayer_cron_job/')
import unittest
from database import Database
import configparser
from entries import Dummy
from datetime import datetime, timedelta
      
config = configparser.ConfigParser()
with open(r'scheduler.conf') as f:
    config.read_file(f)
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

    def test_bbbb_delete_due_recs(self):
        print("DELETE OLD RECORDS")
        due = database.fetch_due_actions()
        self.assertEqual(due[0][0], 'Due')
        database.delete_expired_records()
        database.cursor.execute("select * from delayer where delayer_db_internal_comment='Due'")
        self.assertTrue(database.cursor.fetchall() == [])


    def test_cccc_ensure_new(self):
        print("ENSURE NOT DUE IS THERE")
        database.cursor.execute("select * from delayer where delayer_db_internal_comment='Not due'")
        res = database.cursor.fetchall()
        self.assertTrue(len(res) > 0)


if __name__ == '__main__': 
    unittest.main() 
