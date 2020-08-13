from abc import ABC, abstractmethod 
import psycopg2 
import pytz
from datetime import datetime, timedelta
from salesforce import Salesforce 
import psycopg2.extras

class Operator(ABC):
    def __init__(self, config, operator_type):
        self.conn = psycopg2.connect(
            database = config.get('database','DB_NAME'),
            user = config.get('database','DB_USER'), 
            password = config.get('database','DB_PASSWORD'), 
            host = config.get('database','DB_HOST'), 
            port = config.get('database','DB_PORT'),
        )
        self.conn.autocommit = True  
        self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        if operator_type not in ['delayer_v2', 'reminder']:
            raise Exception("Unknown operator type")
        self.operator = operator_type
        self.config = config
        self.now_rounded = datetime.now(pytz.timezone('America/New_York')).replace(minute=0).strftime("%Y-%m-%d %H:%M")

    @abstractmethod
    def update_records_before_trigger(self):
        pass

    @abstractmethod
    def fetch_due_actions(self):
        pass
    
    @abstractmethod
    def update_records_after_trigger(self):
        pass

    def get_lead_ids(self):
        self.cursor.execute(f"SELECT DISTINCT lead_id FROM {self.operator};")
        return [row[0] for row in self.cursor.fetchall()]

    def add_salesforce_records(self, data, names):
        placeholders = ",".join(["(%s,%s,%s,%s,%s,%s)" for i in data])
        field_names = ",".join(names)
        recs_array = []
        for dic in data:
            for field in names:
                recs_array.append(dic[field])
                
        self.cursor.execute(
        f'''
            INSERT INTO salesforce_recs ({field_names})
            VALUES {placeholders}
        ''', recs_array)

    def get_salesforce_data(self):
        s = Salesforce(self.config)
        s.authenticate()
        boolean_fields, date_fields = s.get_object_fields()
        lead_ids = self.get_lead_ids()
        recs = s.get_classified_records(lead_ids,boolean_fields+["PRECON_DATE__c","PREDEMO_DATE__c"])
        self.add_salesforce_records(recs,["id","name", "satisfied", "not_satisfied","status", "START_DATE"])


    def sync_start_dates_w_salesforce(self):
        reminder_condition = ""
        if self.operator != "delayer":
            reminder_condition = "AND (trigger_date_definition).next_date < sf.START_DATE - (trigger_date_definition).days_before_start * interval '1 day'"
        self.cursor.execute(
            f'''
            UPDATE {self.operator} as op
            SET trigger_date_definition.next_date = sf.START_DATE::timestamp - (trigger_date_definition).days_before_start * interval '1 day'
            FROM salesforce_recs as sf
            WHERE sf.id = op.lead_id
            AND (trigger_date_definition).next_date != sf.START_DATE::timestamp - (trigger_date_definition).days_before_start * interval '1 day'
            {reminder_condition}
            RETURNING *;
            ''', [self.now_rounded, self.now_rounded ])
        updated = self.cursor.fetchall()
        for d in updated:
            self.print_record(f"{self.operator} DATABASE UPDATED BASED ON PRECON/PREDEMO",d)
        return updated

    def truncate_salesforce_records(self):
        self.cursor.execute("TRUNCATE SALESFORCE_RECS;")


    def perform_trigger_actions(self):
        due_actions = self.fetch_due_actions()
        for action in due_actions:
            url_to_hit = config.get('urls',action[2])
            lead_id = action['lead_id']
            tag = action['tag']
            additional_info = action['additional_info']
            requests.post(url_to_hit, data={'lead_id':lead_id, 'internal_tag':tag, 'additional_info':additional_info})
            self.print_record(f"{self.operator}: Triggered ",action)
            sleep(1)




    def print_record(self, prefix, record):
        self.cursor.execute(f'''
            select column_name 
            from information_schema.columns 
            where table_name = '{self.operator}'; 
        ''')
        fields = [row[0] for row in self.cursor.fetchall()]
        log = ""
        for num,name in enumerate(fields):
            field_value = record[num]
            if isinstance(field_value , datetime):
                log+=f"{name}: {record[num].strftime('%Y-%m-%d %H:%M')} -- "
            else:
                log += f"{name}: {record[num]} -- "
        print(f"{prefix} | {log}")
        print("--------------")


    def add_new_record(self,db_fields): 
        table_names = [key for key in db_fields.keys() ]
        values = [db_fields[key] for key in db_fields.keys() ]
        values_placeholders = ",".join(["%s" for i in values])
        self.cursor.execute(
            f'''
            INSERT INTO {self.operator} ({",".join(table_names)})
            VALUES 
            ({values_placeholders})
            ''',values)



