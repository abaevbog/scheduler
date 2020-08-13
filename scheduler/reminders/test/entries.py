
class Dummy:
    def __init__(self):
        self.salesforce_entries = [
            {'id':'1',
            'name':'not satisfied, not expired, not due ',
            'status':'TEST',
            "satisfied": [], 
            "not_satisfied":[],
            'START_DATE': '2020-10-12 13:00:00'}, 
            {'id':'2',
            'name':'not satisfied, not expired, due ',
            'status':'TEST',
            "satisfied": [], 
            "not_satisfied":[],
            'START_DATE': '2020-08-30 12:00:00'},
            {'id':'3',
            'name':'not satisfied, expired',
            'status':'TEST',
            "satisfied": [], 
            "not_satisfied":[],
            'START_DATE': '2020-07-20 13:00:00'},
            {'id':'4',
            'name':'satisfied ',
            'status':'TEST',
            "satisfied": ['existing_field'], 
            "not_satisfied":[],
            'START_DATE': '2020-10-14 13:00:00'},              
        ]
        self.database_entries  = [
            {
            'lead_id': '1',
            'project_name': 'start day corect, not satisfied, not expired, not due ',
            'tag': 'vp-01-01',
            'cutoff': (8,5,10),
            'required_salesforce_fields': ['field'],
            'trigger_date_definition': (7,'2020-10-05 13:00:00'),
            'id':1
        },
            {
            'lead_id': '2',
            'project_name': 'start day corect, not satisfied, not expired, due, after cutoff ',
            'tag': 'vp-01-01',
            'cutoff': (20,5,10),
            'required_salesforce_fields': ['field'],
            'trigger_date_definition': (17,'2020-08-13 12:00:00'),
            'id':2
        },
            {
            'lead_id': '3',
            'project_name': 'start day corect, not satisfied, expired',
            'tag': 'vp-01-01',
            'cutoff': (8,5,10),
            'required_salesforce_fields': ['field'],
            'trigger_date_definition': (14,'2020-07-06 13:00:00'),
            'id':3
        },
            {
            'lead_id': '4',
            'project_name': 'start day corect, satisfied',
            'tag': 'vp-01-01',
            'cutoff': (8,5,10),
            'required_salesforce_fields': ['existing_field'],
            'trigger_date_definition': (7,'2020-10-07 13:00:00'), 
            'id':4
        },
            {# start: 2020-10-12 13:00:00
            # start-wait_for: 2020-10-05
            'lead_id': '1',
            'project_name': 'start day INcorect, no update (close to start date), not satisfied, not expired, not due ',
            'tag': 'vp-01-02',
            'cutoff': (8,5,10),
            'required_salesforce_fields': ['field'],
            'trigger_date_definition': (7,'2020-10-10 13:00:00'),
            'id':5
        },
            {#start: 2020-08-20 12:00:00
            # start-wait_for: 2020-08-13
            'lead_id': '2',
            'project_name': 'start day INcorect,UPDATE, not satisfied, not expired, due, before cutoff ',
            'tag': 'vp-01-02',
            'cutoff': (10, 5, 10),
            'required_salesforce_fields': ['field'],
            'trigger_date_definition': (17,'2020-08-10 12:00:00'),
            'id':6
        },
            {# start: 2020-07-20 13:00:00
            # start-wait_for: 2020-07-06
            'lead_id': '3',
            'project_name': 'start day INcorect,UPDATE, not satisfied, expired',
            'tag': 'vp-01-02',
            'cutoff': (8,5,10),
            'required_salesforce_fields': ['field'],
            'trigger_date_definition': (14,'2020-07-03 13:00:00'),
            'id':7
        },
            {# start: 2020-10-14 13:00:00
            # start-wait_for: 2020-10-07
            'lead_id': '4',
            'project_name': 'start day INcorect,no update (close to start date), satisfied',
            'tag': 'vp-01-02',
            'cutoff': (8,5,10),
            'required_salesforce_fields': ['existing_field'],
            'trigger_date_definition': (7,'2020-10-10 13:00:00'),
            'id':8
        }
        ]