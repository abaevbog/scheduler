import sys
sys.path.append('/Users/bogdanabaev/RandomProgramming/BasementRemodeling/scheduler/scheduler_cron_job/')
from salesforce import Salesforce
import unittest
from database import Database
import boto3
import configparser
from entries import Dummy
from runner import delete_satisfied_records
import pytz
from datetime import datetime, timedelta
      
config = configparser.ConfigParser()
with open(r'scheduler.conf') as f:
    config.read_file(f)
salesforce = Salesforce(config)
database = Database(config)
token = salesforce.authenticate()

class Testing(unittest.TestCase):

    def test_aaaaaa_db_setup(self):
        print("DB SETUP")
        database.create_main_table()
        dummy = Dummy()
        database.add_new_record(**dummy.param_one)
        database.add_new_record(**dummy.param_two_email)
        database.add_new_record(**dummy.param_two_text)
        database.add_new_record(**dummy.param_three)
        database.add_new_record(**dummy.param_four)
        database.add_new_record(**dummy.param_five)
        database.add_new_record(**dummy.param_seven)
        database.create_salesforce_recs_table()     

    def test_cccdddd_delete_old_recs(self):
        print("DELETE OLD RECORDS")
        database.delete_expired_records()
        database.cursor.execute("select * from scheduler where reminders_db_internal_comment='Action due but event date reached.'")
        self.assertTrue(database.cursor.fetchall() == [])


    def test_ccccccc_expire_satisfied_records(self):
        print("EXPIRE SATISFIED RECORDS")
        delete_satisfied_records(database, salesforce)
        database.cursor.execute("select * from scheduler where reminders_db_internal_comment LIKE 'Satisfied%'")
        self.assertTrue(database.cursor.fetchall() == [])

    def test_ddddddd_due_actions(self):
        print("ACTIONS DUE")
        due_actions = database.fetch_due_actions()
        comments = [rec[0] for rec in due_actions]
        self.assertIn('Next action due, after cutoff',comments )
        self.assertIn('Next action due, before cutoff' , comments )
        self.assertIn('One time field that should be expired.' , comments)


    def test_eeeeeeee_update_next_action_date(self):
        print("UPDATE ACTIONS")
        tz = pytz.timezone('America/New_York')
        one_day_from_now = datetime.now(tz) + timedelta(days = 1 )
        one_day_from_now = one_day_from_now.strftime("%Y-%m-%d %H:%M")
        three_days_from_now = datetime.now(tz) + timedelta(days = 3 )
        three_days_from_now = three_days_from_now.strftime("%Y-%m-%d %H:%M")
        database.update_next_dates_of_due_actions()
        database.cursor.execute("select * from scheduler where reminders_db_internal_comment LIKE '% after cutoff'")
        self.assertEqual(str(database.cursor.fetchone()[3].strftime("%Y-%m-%d %H:%M"))[:10], one_day_from_now[:10])
        database.cursor.execute("select * from scheduler where reminders_db_internal_comment LIKE '% before cutoff'")
        self.assertEqual(str(database.cursor.fetchone()[3].strftime("%Y-%m-%d %H:%M"))[:10], three_days_from_now[:10])


if __name__ == '__main__': 
    unittest.main() 
