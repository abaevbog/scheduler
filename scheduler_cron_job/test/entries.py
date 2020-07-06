
class Dummy:
    def __init__(self):
        # don't do anything to this one
        self.param_one = {
            'lead_id': '00Qf400000OV4zKEAT',
            'reminders_db_internal_tag': 'Client Form 1',
            'next_action': '2020-07-26 18:00',
            'event_date': '2020-07-29 18:00',
            'cutoff':None,
            'type':None,
            'url_to_hit':None,
            'frequency_in_days_before_cutoff':None,
            'frequency_in_days_after_cutoff': None,
            'required_salesforce_fields' : None,
            'reminders_db_internal_comment' : 'This should not be touched'
        }
        # one time, no renew. it's due, and then should be deleted
        self.param_four = {
            'lead_id': '00Qf400000OV4zKEAT',
            'reminders_db_internal_tag': 'Client Form 1',
            'next_action': '2020-06-24 18:00',
            'event_date': '2020-07-29 18:00',
            'cutoff':None,
            'type':None,
            'url_to_hit':None,
            'frequency_in_days_before_cutoff':None,
            'frequency_in_days_after_cutoff': None,
            'required_salesforce_fields' : None,
            'reminders_db_internal_comment' : 'One time field that should be expired.'
        }

        #satisfied record
        self.param_two_email = {
            'lead_id': '00Qf400000NSD7oEAH',
            'reminders_db_internal_tag': 'Client Form 1',
            'next_action': '2020-06-24 18:00',
            'event_date': '2020-07-29 18:00',
            'cutoff':'2020-06-23 18:00',
            'type': 'EMAIL',
            'url_to_hit':None,
            'frequency_in_days_before_cutoff':3,
            'frequency_in_days_after_cutoff': 1,
            'required_salesforce_fields' : ['start_date_confirmed__c', 'project_prep_form_submitted__c'],
            'reminders_db_internal_comment' : 'Satisfied record text'
        }
        # satisfied record
        self.param_two_text = {
            'lead_id': '00Qf400000NSD7oEAH',
            'reminders_db_internal_tag': 'Client Form 1',
            'next_action': '2020-06-24 18:00',
            'event_date': '2020-07-29 18:00',
            'cutoff':'2020-06-23 18:00',
            'type': 'TEXT',
            'url_to_hit':None,
            'frequency_in_days_before_cutoff':3,
            'frequency_in_days_after_cutoff': 1,
            'required_salesforce_fields' : ['start_date_confirmed__c', 'project_prep_form_submitted__c'],
            'reminders_db_internal_comment' : 'Satisfied record email'
        }
        # due action: after cutoff
        self.param_three = {
            'lead_id': '00Qf400000NSD7oEAH',
            'reminders_db_internal_tag': 'Client Form 2',
            'next_action': '2020-06-24 18:00',
            'event_date': '2020-07-29 18:00',
            'cutoff':'2020-06-23 18:00',
            'type': 'TEXT',
            'url_to_hit':None,
            'frequency_in_days_before_cutoff':3,
            'frequency_in_days_after_cutoff': 1,
            'required_salesforce_fields' : ['start_date_confirmed__c', 'project_prep_form_submitted__c','impossible_field'],
            'reminders_db_internal_comment' : 'Next action due, after cutoff'
        }
        # due action before cutoff
        self.param_five = {
            'lead_id': '00Qf400000OV8YPEA1',
            'reminders_db_internal_tag': 'Client Form 2',
            'next_action': '2020-06-24 18:00',
            'event_date': '2020-07-29 18:00',
            'cutoff': '2020-06-26 18:00',
            'type':'TEXT',
            'url_to_hit':None,
            'frequency_in_days_before_cutoff':3,
            'frequency_in_days_after_cutoff': 1,
            'required_salesforce_fields' : ['start_date_confirmed__c', 'project_prep_form_submitted__c','impossible_field'],
            'reminders_db_internal_comment' : 'Next action due, before cutoff'
        }
        # past event date: delete
        self.param_seven = {
            'lead_id': '00Qf400000OV8YPEA1',
            'reminders_db_internal_tag': 'Client Form 2',
            'next_action': '2020-06-30 18:00',
            'event_date': '2020-06-29 18:00',
            'cutoff':'2020-06-23 18:00',
            'type': 'TEXT',
            'url_to_hit':None,
            'frequency_in_days_before_cutoff':3,
            'frequency_in_days_after_cutoff': 1,
            'required_salesforce_fields' : ['start_date_confirmed__c', 'project_prep_form_submitted__c','impossible_field'],
            'reminders_db_internal_comment' : 'Action due but event date reached.'
        }