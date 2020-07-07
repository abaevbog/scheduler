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
    db.delayer.add_record(**body)
    return {"statusCode":200, "body": json.dumps({"message" : "Record added to DB"})}

def request_fields(event,context):
    fields = db.delayer.get_fields()
    return {"statusCode":200, "body": json.dumps({"db_fields" : fields})}