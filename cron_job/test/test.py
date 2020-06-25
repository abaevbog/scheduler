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
        self.salesforce = Salesforce(config,token='00Df40000025Uc7!AQoAQJfPxiv.QNUb4_R4Da8g1d5JVxehlbZqXfGtmsUYz9916K9.WLv2_DjUZbGB0lxR1g_JN2B7AgrGxX3aHI_6W1essm_B')
        self.database = Database(config)
        token = self.salesforce.authenticate()
        self.database.create_main_table()
        print(token)
        #print("DB created")
        #dummy = Dummy()
        #self.database.add_new_record(**dummy.param_one)
        #self.database.add_new_record(**dummy.param_two)
        #self.database.add_new_record(**dummy.param_three)
        #print("Records added")


    def test_salesforce_workflow(self):
        checkbox_fields, date_fields  = self.salesforce.get_object_fields()
        self.salesforce.get_records(['00Qf400000OV4zKEAT', '00Qf400000NSD7oEAH', '00Qf400000OV8YPEA1'],list(set(checkbox_fields)) )
        self.salesforce.write_records_to_s3(['00Qf400000OV4zKEAT', '00Qf400000NSD7oEAH', '00Qf400000OV8YPEA1'],list(set(checkbox_fields)))
        self.assertTrue('FOO'.isupper())

    
    def test_secondary_db(self):
        checkbox_fields, date_fields  = self.salesforce.get_object_fields()   
        print(f"boolean fields in test seondary db: {checkbox_fields}")  
        self.database.create_salesforce_recs_table(checkbox_fields)
        self.database.import_data_from_s3()

if __name__ == '__main__': 
    unittest.main() 
