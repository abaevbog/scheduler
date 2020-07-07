from database import Database
from salesforce import Salesforce
from time import sleep
import requests 
import os
import configparser
import sys

# fetch all actions, check with salesforce
# for all records that have all prerequisites satisfied
# delete them. 
def delete_satisfied_records(db,salesforce):
    # get all up to date boolean fields from salesforce
    boolean_fields, date_fields = salesforce.get_object_fields()
    # get all lead ids from db
    all_lead_ids = db.fetch_all_lead_ids()
    if all_lead_ids == []:
        return
    # fetch records with given lead ids and write them to salesforce records table
    recs = salesforce.get_parsed_records(all_lead_ids,boolean_fields)
    db.insert_data_to_salesforce_recs(recs)
    # then, for every type of notification (text, email, other)
    # we want to perform a join with scheduler and status table
    # to get table with all required fields and all satisfied fields
    satisfied_entries = db.find_satisfied_records()
    deleted = db.delete_records(satisfied_entries)
    for d in deleted:
        db.print_record("SCHEDULER DATABASE SATISFIED", d)


def main():
    print("SCHEDULER: EXECUTION BEGAN")
    config = configparser.ConfigParser()
    config.read('scheduler.conf')
    database = Database(config)
    salesforce = Salesforce(config)
    salesforce.authenticate()
    print("SCHEDULER: SALESFORCE AUTHENTICATION COMPLETE")
    # delete records that have been satisfied to not 
    # send people reminders about things they did
    delete_satisfied_records(database, salesforce)
    print("SCHEDULER: SATISFIED RECORDS REMOVED")
    # now, delete all entries that reached their expiration date
    database.delete_expired_records()
    # find what actions are to be activated or reminded now
    due_actions = database.fetch_due_actions()
    # go through all records, hit correct urls
    print("SCHEDULER: DUE ACTIONS FETCHED")
    for action in due_actions:
        url_to_hit = config.get('urls',action[2])
        lead_id = action[1]
        reminders_db_internal_tag = action[2]
        action_type = action[7]
        requests.post(url_to_hit, data={'lead_id':lead_id, 'internal_tag':reminders_db_internal_tag, 'type':action_type}) #we'll have to send more stuff in body. What other fields should be sent?
        print(f"SCHEDULER: Triggered event for {lead_id} with status {reminders_db_internal_tag}")
        # sleep to not overload api gateway
        sleep(1)
    print("SCHEDULER: ALL ACTIONS TAKEN")

    print("SCHEDULER: ONE TIME RECORDS EXPIRED")
    # update when renewable actions should be triggered next
    database.update_next_dates_of_due_actions()
    print("SCHEDULER: NEXT DATES UPDATED")
    # toss away old status table
    database.truncate_salesforce_records()
    print("SCHEDULER:DONE")
    database.connection.close()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        sys.exit(1)
