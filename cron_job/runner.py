from database import Database
from salesforce import Salesforce
from time import sleep
import requests 
import os
import configparser
# fetch all actions, check with salesforce
# for all records that have all prerequisites satisfied
# delete them. Probably adjust salesforce module
def expire_satisfied_records(db,salesforce):
    # get all up to date boolean fields from salesforce
    boolean_fields, date_fields = salesforce.get_object_fields()
    # get all lead ids from db
    all_lead_ids = db.fetch_all_lead_ids()
    # fetch records with given lead ids and write them to s3
    salesforce.write_records_to_s3(all_lead_ids,boolean_fields)
    # toss away old status table and load new data into it
    db.reload_salesforce_records()
    db.export_data_from_s3()
    # then, for every type of notification (text, email, other)
    # we want to perform a join with scheduler and status table
    # to get table like: lead_idFIELDS_REQUIRED FIELD_ONE(true/false) FIELD_TWO(true/false)
    old_entries = db.find_satisfied_records()
    db.delete_records(old_entries)


def main():
    config = configparser.ConfigParser()
    config.read_file(open(r'scheduler.conf'))
    database = Database(config)
    salesforce = Salesforce(config)
    salesforce.authenticate()
    # delete records that have been satisfied to not 
    # send people reminders about things they did
    expire_satisfied_records(database)

    # find what actions are to be activated or reminded now
    due_actions = database.fetch_due_actions()
    # go through all records, hit correct urls
    for action in due_actions:
        url_to_hit = config.get('urls',action[2])
        lead_id = action[1]
        requests.post(url_to_hit, body={'lead_id':lead_id}) #we'll have to send more stuff in body. What other fields should be sent?
        # sleep to not overload api gateway
        sleep(1)
    # now, delete all entries that should not be renewed
    database.delete_expired_one_time_records()
    # update when renewable actions should be triggered next
    database.update_next_dates_of_due_actions()


if __name__ == "__main__":
    sleep(10)
    #main()
