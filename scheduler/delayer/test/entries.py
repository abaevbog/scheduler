
class Dummy:
    def __init__(self):
        self.salesforce_entries = [
            {'id':'1',
            'name':'start day corect, due',
            'status':'TEST',
            "satisfied": [], 
            "not_satisfied":[],
            'START_DATE': '2020-08-12 13:00:00'},
            {'id':'2',
            'name':'start day corect, not due',
            'status':'TEST',
            "satisfied": [], 
            "not_satisfied":[],
            'START_DATE': '2020-10-20 13:00:00'},
            {'id':'3',
            'name':'start day incorect, due',
            'status':'TEST',
            "satisfied": [], 
            "not_satisfied":[],
            'START_DATE': '2020-08-20 13:00:00'},
            {'id':'4',
            'name':'start day incorect, not due',
            'status':'TEST',
            "satisfied": [], 
            "not_satisfied":[],
            'START_DATE': '2020-11-10 13:00:00'}              
        ]
        self.database_entries  = [
            {
            'lead_id': '1',
            'project_name': 'correct start, due',
            'tag': 'vp-01-01',
            'trigger_date_definition': (7,'2020-08-05 13:00:00')
        },
            {
            'lead_id': '2',
            'project_name': 'correct start, not due',
            'tag': 'vp-01-01',
            'trigger_date_definition': (7,'2020-10-13 13:00:00')
        },
            {
            'lead_id': '3',
            'project_name': 'start day incorect, due',
            'tag': 'vp-01-01',
            'trigger_date_definition': (14,'2020-10-07 13:00:00')
        },
            {
            'lead_id': '4',
            'project_name': 'start day incorect, not due',
            'tag': 'vp-01-01',
            'trigger_date_definition': (7,'2020-10-07 13:00:00')
        },{
            'lead_id': '00Qf400000PofRcEAJ',
            'project_name': 'start day incorect, not due',
            'tag': 'vp-01-01',
            'trigger_date_definition': (7,'2020-10-07 13:00:00')
        },

        ]
