import sys
import os
sys.path.insert(1,os.getcwd() + "/db")
from database import Database
import json

database =  os.environ['DB_NAME'],
user = os.environ['DB_USER'], 
password = os.environ['DB_PASSWORD'], 
host = os.environ['DB_HOST'], 
port = os.environ['DB_PORT']
config = {'database':database[0],'user':user[0],'password':password[0],'host':host[0],'port':port }
db = Database(config)



def add(event,context):
    body = json.loads(event['body'])
    db.scheduler.add_record(**body)
    return {"statusCode":200, "body": json.dumps({"message" : "Record added to DB"})}

def request_fields(event,context):
    fields = db.scheduler.get_fields()
    return {"statusCode":200, "body": json.dumps({"db_fields" : fields})}

def update(event,context):
    body = json.loads(event['body'])
    new_cutoff = body['cutoff']
    new_event_date = body['event_date']
    lead_id = body['lead_id']
    next_action = None
    if 'next_action' in body.keys():
        next_action = body['next_action']
    db.scheduler.update_record(lead_id,new_cutoff,new_event_date,new_next_action=next_action)
    return {"statusCode":200, "body": json.dumps({"message" : 'Record(s) updated'})}

def delete_record(event,context):
    body = json.loads(event['body'])
    internal_tag = body['internal_tag']
    lead_id = body['lead_id']
    db.delayer.delete_record(lead_id,internal_tag)
    return {"statusCode":200, "body": json.dumps({"message" : "Record deleted"})}