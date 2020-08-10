
class Dummy:
    def __init__(self):
        # don't do anything to this one
        self.param_one = {
            'delayer_db_internal_tag': 'vp-01-01a',
            'lead_id':'00Qf400000OV4zKEAT',
            'delayer_db_internal_comment': 'Not due',
            'trigger_date': '2020-09-26 18:00',
            'additional_info': None
        }
        # due, delete
        self.param_two = {
            'delayer_db_internal_tag': 'vp-01-01a',
            'lead_id':'00Qf400000OV4zKEAT',
            'delayer_db_internal_comment': 'Due',
            'trigger_date': '2020-06-26 18:00',
            'additional_info': None
        }
        # entry to be updated 7 days before precon
        self.param_three = {
            'delayer_db_internal_tag': 'vp-01-01a',
            'lead_id':'00Qf400000OV4zKEAT',
            'delayer_db_internal_comment': 'Precon date TO BE UPDATED',
            'trigger_date': '2020-06-26 18:00',
            'wait_for_precon_or_predemo': 'PRECON',
            'days_before_precon_or_predemo' : 7
        }
        
        # entry to not be updated with precon
        self.param_four = {
            'delayer_db_internal_tag': 'vp-01-01a',
            'lead_id':'00Qf400000OV4zKEAT',
            'delayer_db_internal_comment': 'Predemo date no update',
            'trigger_date': '2020-08-02 12:00:00',
            'wait_for_precon_or_predemo': 'PREDEMO',
            'days_before_precon_or_predemo' : 2
        }
