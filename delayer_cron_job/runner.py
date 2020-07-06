from database import Database
from time import sleep
import requests 
import os
import configparser


def main():
    print("DELAYER: EXECUTION BEGAN")
    config = configparser.ConfigParser()
    config.read('scheduler.conf')
    database = Database(config)
    # find what actions are to be activated or reminded now
    due_actions = database.fetch_due_actions()
    # go through all records, hit correct urls
    print("DELAYER: DUE ACTIONS FETCHED")
    for action in due_actions:
        url_to_hit = config.get('urls',action[2])
        lead_id = action[1]
        delayer_db_internal_tag = action[2]
        requests.post(url_to_hit, data={'lead_id':lead_id, 'internal_tag':delayer_db_internal_tag})
        print(f"DELAYER: Triggered event for {lead_id} with {delayer_db_internal_tag}")
        # sleep to not overload api gateway
        sleep(1)
    print("DELAYER: ALL ACTIONS TAKEN")
    # now, delete all old entries 
    database.delete_expired_records()
    print("DELAYER: OLD RECORDS EXPIRED")
    database.connection.close()
    print("DELAYER: DONE")


if __name__ == "__main__":
    main()
