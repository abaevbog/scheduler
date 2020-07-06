
class Dummy:
    def __init__(self):
        # don't do anything to this one
        self.param_one = {
            'delayer_db_internal_tag': 'vp-01-01a',
            'lead_id':'00Qf400000OV4zKEAT',
            'delayer_db_internal_comment': 'Not due',
            'trigger_date': '2020-07-26 18:00',
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
