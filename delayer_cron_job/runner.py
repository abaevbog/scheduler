from database import Database
from salesforce import Salesforce
from time import sleep
import requests 
import os
import configparser
import sys

def update_precon_or_predemo_dependend_entries(db,salesforce):
    # get all lead ids from db
    all_lead_ids = db.fetch_all_lead_ids()
    if all_lead_ids == []:
        return
    # fetch records with given lead ids
    recs = salesforce.get_records(all_lead_ids)
    db.insert_salesforce_data(recs)
    # then, we need to update action date for those fields that
    # depend on precon/predemo
    db.update_start_date_depending_on_precon()

def main():
    #print("DELAYER: EXECUTION BEGAN")
    config = configparser.ConfigParser()
    config.read('scheduler.conf')
    database = Database(config)
    salesforce = Salesforce(config)
    update_precon_or_predemo_dependend_entries(database,salesforce)
    # find what actions are to be activated or reminded now
    due_actions = database.fetch_due_actions()
    # go through all records, hit correct urls
    for action in due_actions:
        url_to_hit = config.get('urls',action[2])
        lead_id = action[1]
        delayer_db_internal_tag = action[2]
        additional_info = action[4]
        requests.post(url_to_hit, data={'lead_id':lead_id, 'internal_tag':delayer_db_internal_tag, 'additional_info':additional_info})
        database.print_record("DELAYER: Triggered",action)
        # sleep to not overload api gateway
        sleep(1)
    #print("DELAYER: ALL ACTIONS TAKEN")
    # now, delete all old entries 
    database.delete_expired_records()
    #print("DELAYER: OLD RECORDS EXPIRED")
    database.connection.close()
    #print("DELAYER: DONE")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        sys.exit(1)
