import sys
sys.path.append('/usr/src/app/')
from salesforce import Salesforce
import unittest
from database import Database
import boto3
import configparser
from entries import Dummy
from runner import expire_satisfied_records
import pytz
from datetime import datetime
      
config = configparser.ConfigParser()
with open(r'../scheduler.conf') as f:
    config.read_file(f)
salesforce = Salesforce(config,token='00Df40000025Uc7!AQoAQPb4BTmeMXplIODsMXaQ2DXHBvpYzuFH2hQdBWLuCTr1dJWhF6GfbgacAYF02s_AkXEkuFPtNgP63Eikk6HLTDj.mY.Q')
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
        

    def test_bbbbbb_secondary_db(self):
        print("SECONDARY DB SETUP")
        checkbox_fields, date_fields  = salesforce.get_object_fields() 
        database.create_salesforce_recs_table()
        recs = salesforce.get_parsed_records(['00Qf400000OV4zKEAT', '00Qf400000NSD7oEAH', '00Qf400000OV8YPEA1'],list(set(checkbox_fields)))

    def test_ccccccc_expire_satisfied_records(self):
        print("EXPIRE SATISFIED RECORDS")
        expire_satisfied_records(database, salesforce)
        database.cursor.execute("select * from scheduler where comment LIKE 'Satisfied%'")
        self.assertTrue(database.cursor.fetchall() == [])

    def test_ddddddd_due_actions_and_one_time_expiration(self):
        print("ACTIONS DUE")
        due_actions = database.fetch_due_actions()
        comments = [rec[-1] for rec in due_actions]
        self.assertIn('Next action due, after cutoff',comments )
        self.assertIn('Next action due, before cutoff' , comments )
        self.assertIn('One time field that should be expired.' , comments)
        database.delete_expired_one_time_records()
        database.cursor.execute("select * from scheduler where comment='One time field that should be expired.'")
        self.assertTrue(database.cursor.fetchall() == [])

    def test_eeeeeeee_update_next_action_date(self):
        print("UPDATE ACTIONS")
        database.update_next_dates_of_due_actions()
        database.cursor.execute("select * from scheduler where comment LIKE '% after cutoff'")
        self.assertEqual(str(database.cursor.fetchone()[3].strftime("%Y-%m-%d %H:%M")), '2020-06-25 18:00')
        database.cursor.execute("select * from scheduler where comment LIKE '% before cutoff'")
        self.assertEqual(str(database.cursor.fetchone()[3].strftime("%Y-%m-%d %H:%M")), '2020-06-27 18:00')


if __name__ == '__main__': 
    unittest.main() 
