import boto3
import requests
from database import Database
import json
import os

database =  os.environ['DB_NAME'],
user = os.environ['DB_USER'], 
password = os.environ['DB_PASSWORD'], 
host = os.environ['DB_HOST'], 
port = os.environ['DB_PORT']
config = {'database':database[0],'user':user[0],'password':password[0],'host':host[0],'port':port }
db = Database(config)

def add(event,context):
    body = json.loads(event['body'])
    db.add_new_record(**body)
    return {"statusCode":200, "body": json.dumps({"message" : "Record added to DB"})}


def delete(event,context):
    lead_id = event['queryStringParameters']['lead_id']
    db.delete_record(lead_id)
    return {"statusCode":200, "body": json.dumps({"message" : "Record removed"})}

def request_fields(event,context):
    print("Requesting fields")
    fields = db.get_fields()
    return {"statusCode":200, "body": json.dumps({"db_fields" : fields})}

def create_tables(event,context):
    print("Creating tables")
    db.create_reminders_table()
    db.create_salesforce_recs_table()
    db.create_delays_table()
    return {"statusCode":200, "body": json.dumps({"message" : "Tables created!"})}


