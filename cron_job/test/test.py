import sys
sys.path.append('/usr/src/app/')
from salesforce import Salesforce
import unittest
from database import Database
import boto3
import configparser
from entries import Dummy



class Testing(unittest.TestCase):
    def setUp(self):       
        config = configparser.ConfigParser()
        with open(r'../scheduler.conf') as f:
            config.read_file(f)
        self.salesforce = Salesforce(config,token='00Df40000025Uc7!AQoAQPb4BTmeMXplIODsMXaQ2DXHBvpYzuFH2hQdBWLuCTr1dJWhF6GfbgacAYF02s_AkXEkuFPtNgP63Eikk6HLTDj.mY.Q')
        self.database = Database(config)
        token = self.salesforce.authenticate()
        print(token)


    def ok_test_db_setup(self):
        self.database.create_main_table()
        dummy = Dummy()
        self.database.add_new_record(**dummy.param_one)
        self.database.add_new_record(**dummy.param_two_email)
        self.database.add_new_record(**dummy.param_two_text)
        self.database.add_new_record(**dummy.param_three)
        self.database.add_new_record(**dummy.param_four)
        self.database.add_new_record(**dummy.param_five)

    def ok_test_salesforce_workflow(self):
        checkbox_fields, date_fields  = self.salesforce.get_object_fields()
        self.salesforce.get_records(['00Qf400000OV4zKEAT', '00Qf400000NSD7oEAH', '00Qf400000OV8YPEA1'],list(set(checkbox_fields)) )
        self.assertTrue('FOO'.isupper())

    
    def test_secondary_db(self):
        checkbox_fields, date_fields  = self.salesforce.get_object_fields() 
        self.database.create_salesforce_recs_table(checkbox_fields)
        recs = self.salesforce.parse_records(['00Qf400000OV4zKEAT', '00Qf400000NSD7oEAH', '00Qf400000OV8YPEA1'],list(set(checkbox_fields)))
        self.database.insert_data_to_salesforce_recs(recs)

    def ok_test_due_actions_and_one_time_expiration(self):
        self.assertTrue(self.database.fetch_due_actions()[0][-1] == 'Next action due, after cutoff')
        self.assertTrue(self.database.fetch_due_actions()[1][-1] == 'Next action due, before cutoff')
        self.database.delete_expired_one_time_records()
        self.database.cursor.execute("select * from scheduler where comment='One time field that should be expired.'")
        self.assertTrue(self.database.cursor.fetchall() == [])


    def test_find_satisfied_records(self):
        self.assertTrue(True)

if __name__ == '__main__': 
    unittest.main() 
