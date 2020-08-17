import sys
sys.path.insert(1, '/Users/bogdanabaev/RandomProgramming/BasementRemodeling/scheduler/scheduler/') 
from my_operator import Operator


#Reminder:
#0. get updated start dates from salesforce
#1. delete expired records (reached start date)
#2. delete satisfied records (all fields = yes in sf)
#3. fetch due actions
#4. Update records that are past now according to their rules


# CUTOFF DATE doesn't change so far: make it depend on start date
class Reminders(Operator):
    def __init__(self,config):
        super().__init__(config,"reminder")

    def fetch_due_actions(self):
        recs = self.cursor.execute(
            f'''
            SELECT * FROM reminder,salesforce_recs
            WHERE reminder.lead_id = salesforce_recs.id
            AND (reminder).trigger_date_definition.next_date <= %s::timestamp;
            ''',[self.now_rounded])
        return self.cursor.fetchall()

    # delete records that reached event date
    def delete_expired_records(self):
        self.cursor.execute(
            f'''
            DELETE FROM reminder
            WHERE lead_id IN 
            (SELECT lead_id FROM reminder INNER JOIN salesforce_recs
            ON reminder.lead_id = salesforce_recs.id
            WHERE salesforce_recs.start_date <= %s::timestamp
            AND NOT ARRAY['ON_HOLD__c']::varchar[] <@ salesforce_recs.satisfied)
            AND NOT reminder.indefinite
            RETURNING *;
            ''',[self.now_rounded ])
        deleted = self.cursor.fetchall()
        for d in deleted:
            self.print_record("REMINDER EXPIRED",d)
        return deleted


    #  find records that have all necessary checkboxes checked in salesforce
    # or records that are on hold or records that have been cancelled
    def delete_satisfied_records(self):
        self.cursor.execute(
            f'''
            DELETE FROM reminder WHERE id IN
                (SELECT reminder.id FROM reminder INNER JOIN salesforce_recs
                ON reminder.lead_id = salesforce_recs.id
                WHERE ( 
                NOT ARRAY['ON_HOLD__c'] <@ salesforce_recs.satisfied::text[]
                AND (reminder).required_salesforce_fields <@ salesforce_recs.satisfied)
                OR salesforce_recs.status = 'SALE CANCELLED')
            RETURNING *;
            '''
        )
        deleted = self.cursor.fetchall()
        for d in deleted:
            self.print_record('REMINDER SATISFIED DELETED ', d)
        return deleted


    # update date of when the action should be triggered next time
    def update_records_after_trigger(self):
        self.cursor.execute(
            '''
            UPDATE reminder
            SET trigger_date_definition.next_date = %s::timestamp + (cutoff).freq_before * interval '1 day'
            FROM salesforce_recs as sf
            WHERE reminder.lead_id = sf.id
                AND (trigger_date_definition).next_date <= %s::timestamp 
                AND %s::timestamp < sf.START_DATE - (reminder).cutoff.days_before_start * interval '1 day'
            RETURNING *;
            ''', [self.now_rounded, self.now_rounded, self.now_rounded ])
        updated_before = self.cursor.fetchall()
        for x in updated_before:
            self.print_record('REMIMDER UPDATED BEFORE CUTOFF -- ',x)
        updated_ids = [row[8] for row in updated_before]
        self.cursor.execute('''
            UPDATE reminder
            SET trigger_date_definition.next_date = %s::timestamp + (cutoff).freq_after * interval '1 day'
            FROM salesforce_recs as sf
            WHERE reminder.lead_id = sf.id 
                AND (trigger_date_definition).next_date <= %s::timestamp
                AND %s::timestamp >= sf.START_DATE - (reminder).cutoff.days_before_start * interval '1 day'
                AND NOT( reminder.id = ANY(%s))
            RETURNING *;
            ''',[self.now_rounded, self.now_rounded,self.now_rounded ,updated_ids])
        updated_after = self.cursor.fetchall()
        for x in updated_after:
            self.print_record('REMINDER UPDATED AFTER CUTOFF -- ',x)
        return updated_before + updated_after


    def update_records_before_trigger(self):
        self.sync_start_dates_w_salesforce()
        self.delete_expired_records()
        self.delete_satisfied_records()