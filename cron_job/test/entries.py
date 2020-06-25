
class Dummy:
    def __init__(self):
        self.param_one = {
            'lead_id': '00Qf400000OV4zKEAT',
            'lead_status': 'Client Form 1',
            'next_action': '2020-06-26 18:00',
            'event_date': '2020-06-29 18:00',
            'cutoff':None,
            'type':None,
            'url_to_hit':None,
            'frequency_in_days_before_cutoff':None,
            'frequency_in_days_after_cutoff': None,
            'required_salesforce_fields' : None,
            'comment' : 'One time field that should be deleted'
        }

        self.param_two = {
            'lead_id': '00Qf400000NSD7oEAH',
            'lead_status': 'Client Form 1',
            'next_action': '2020-06-24 18:00',
            'event_date': '2020-06-29 18:00',
            'cutoff':'2020-06-23 18:00',
            'type': 'EMAIL',
            'url_to_hit':None,
            'frequency_in_days_before_cutoff':3,
            'frequency_in_days_after_cutoff': 1,
            'required_salesforce_fields' : None,
            'comment' : 'Next action due, after cutoff'
        }

        self.param_three = {
            'lead_id': '00Qf400000OV8YPEA1',
            'lead_status': 'Client Form 2',
            'next_action': '2020-06-24 18:00',
            'event_date': '2020-06-29 18:00',
            'cutoff': '2020-06-26 18:00',
            'type':'TEXT',
            'url_to_hit':None,
            'frequency_in_days_before_cutoff':3,
            'frequency_in_days_after_cutoff': 1,
            'required_salesforce_fields' : None,
            'comment' : 'Next action due, before cutoff'
        }