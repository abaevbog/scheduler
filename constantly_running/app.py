import boto3
import requests
from database import Database
import json
import configparser

config = configparser.ConfigParser()
with open(r'scheduler.conf') as f:
    config.read(f)
db = Database(config)

def add(event,context):
    body = json.loads(event['body'])
    db.add(**body)
    return {"statusCode":200, "body": json.dumps({"message" : "Record added to DB"})}


def delete(event,context):
    lead_id = event['queryStringParameters']['lead_id']
    db.delete_record(lead_id)
    return {"statusCode":200, "body": json.dumps({"message" : "Record removed"})}

def request_fields(event,context):
    fields = db.get_fields()
    return {"statusCode":200, "body": json.dumps({"db_fields" : fields})}




