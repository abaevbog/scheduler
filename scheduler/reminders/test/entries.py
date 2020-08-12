
class Dummy:
    def __init__(self):
        self.salesforce_entries = [
            {'id':'1',
            'name':'start day corect, not satisfied, not expired, not due ',
            'status':'TEST',
            "satisfied": [], 
            "not_satisfied":[],
            'START_DATE': '2020-10-12 13:00:00'},
            {'id':'2',
            'name':'start day corect, not satisfied, not expired, due ',
            'status':'TEST',
            "satisfied": [], 
            "not_satisfied":[],
            'START_DATE': '2020-07-20 13:00:00'},
            {'id':'3',
            'name':'start day corect, not satisfied, expired',
            'status':'TEST',
            "satisfied": [], 
            "not_satisfied":[],
            'START_DATE': '2020-07-20 13:00:00'},
            {'id':'4',
            'name':'start day corect, satisfied ',
            'status':'TEST',
            "satisfied": ['existing_field'], 
            "not_satisfied":[],
            'START_DATE': '2020-10-14 13:00:00'},   
            {'id':'5',
            'name':'start day incorrect',
            'status':'TEST',
            "satisfied": [], 
            "not_satisfied":[],
            'START_DATE': '2020-11-10 13:00:00'},             
        ]
        self.database_entries  = [
            {
            'lead_id': '1',
            'project_name': 'start day corect, not satisfied, not expired, not due ',
            'tag': 'vp-01-01',
            'settings': ("2020-08-06 13:00:00", 7, 7),
            'required_salesforce_fields': ['field'],
            'trigger_date_definition': (7,'2020-10-05 13:00:00')
        },
            {
            'lead_id': '2',
            'project_name': 'start day corect, not satisfied, not expired, due ',
            'tag': 'vp-01-01',
            'settings': ("2020-08-06 13:00:00", 7, 7),
            'required_salesforce_fields': ['field'],
            'trigger_date_definition': (7,'2020-07-13 13:00:00')
        },
            {
            'lead_id': '3',
            'project_name': 'start day corect, not satisfied, expired',
            'tag': 'vp-01-01',
            'settings': ("2020-08-06 13:00:00", 7, 7),
            'required_salesforce_fields': ['field'],
            'trigger_date_definition': (14,'2020-07-06 13:00:00')
        },
            {
            'lead_id': '4',
            'project_name': 'start day corect, satisfied',
            'tag': 'vp-01-01',
            'settings': ("2020-08-06 13:00:00", 7, 7),
            'required_salesforce_fields': ['existing_field'],
            'trigger_date_definition': (7,'2020-10-07 13:00:00')
        }
        ]