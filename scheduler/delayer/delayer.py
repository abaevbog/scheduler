import sys
sys.path.insert(1, '/Users/bogdanabaev/RandomProgramming/BasementRemodeling/scheduler/scheduler/') 
from my_operator import Operator


#delayer_v2:
#0. get updated start dates from salesforce
#1. fetch due actions
#2. delete expired records (reached start date)

class Delayer(Operator):
    def __init__(self,config):
        super().__init__(config,"delayer_v2")

    def fetch_due_actions(self):
        recs = self.cursor.execute(
            f'''
            SELECT * FROM delayer_v2,salesforce_recs
            WHERE delayer_v2.lead_id = salesforce_recs.id
            AND (delayer_v2).trigger_date_definition.next_date <= %s::timestamp;
            ''',[self.now_rounded])
        return self.cursor.fetchall()

    # delete records that reached event date
    def delete_expired_records(self):
        self.cursor.execute(
            f'''
            DELETE FROM delayer_v2
            WHERE id IN 
            (SELECT delayer_v2.id FROM delayer_v2 INNER JOIN salesforce_recs
            ON delayer_v2.lead_id = salesforce_recs.id
            WHERE (delayer_v2).trigger_date_definition.next_date <= %s::timestamp  
            AND NOT ARRAY['ON_HOLD__c']::varchar[] <@ salesforce_recs.satisfied)
            RETURNING *;
            ''',[self.now_rounded ])
        deleted = self.cursor.fetchall()
        for d in deleted:
            self.print_record("delayer EXPIRED",d)



    # update date of when the action should be triggered next time
    def update_records_after_trigger(self):
        self.delete_expired_records()


    def update_records_before_trigger(self):
        self.sync_start_dates_w_salesforce()