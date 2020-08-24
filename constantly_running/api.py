import sys
import os
import json
import configparser
import boto3 
from database import Database
s3 = boto3.client('s3')

database =  os.environ['DB_NAME'],
user = os.environ['DB_USER'], 
password = os.environ['DB_PASSWORD'], 
host = os.environ['DB_HOST'], 
port = os.environ['DB_PORT']
config = {'database':database[0],'user':user[0],'password':password[0],'host':host[0],'port':port }



def add(event,context):
    db = Database(config)
    body = json.loads(event['body'])
    operator = event["queryStringParameters"]['operator']
    if operator == "delayer":
        operator = "delayer_v2"
    elif operator == "reminder":
        body['cutoff'] = tuple(body['cutoff'])
    else:
        raise Exception(f"Unknown operator {operator}")
    body['trigger_date_definition'] = tuple(body['trigger_date_definition'])

    db.add_record(body, operator)
    db.print_record(operator,f"{operator} - ADD ",body)
    return {"statusCode":200, "body": json.dumps({"message" : f"Record added to {operator}"})}

def request_fields(event,context):
    db = Database(config)
    operator = event["queryStringParameters"]['operator']
    if operator == "delayer":
        operator = "delayer_v2"
    elif operator != "reminder":
        raise Exception(f"Unknown operator {operator}")
    fields = db.get_fields(operator)
    return {"statusCode":200, "body": json.dumps({"db_fields" : fields})}

def delete_record(event,context):
    db = Database(config)
    operator = event["queryStringParameters"]['operator']
    if operator == "delayer":
        operator = "delayer_v2"
    elif operator != "reminder":
        raise Exception(f"Unknown operator {operator}")
    body = json.loads(event['body'])
    tag = body['tag']
    lead_id = body['lead_id']
    db.delete_record(lead_id,tag, operator)
    db.print_record(operator, f"{operator} - DELETE ",body)
    return {"statusCode":200, "body": json.dumps({"message" : f"Record deleted from {operator}"})}

def update_record(event,context):
    db = Database(config)
    operator = event["queryStringParameters"]['operator']
    if operator == "delayer":
        operator = "delayer_v2"
    elif operator != "reminder":
        raise Exception(f"Unknown operator {operator}")
    body = json.loads(event['body'])
    tag = body['tag']
    lead_id = body['lead_id']
    trigger_date_def = tuple(body['trigger_date_definition'])
    rec = db.update_record(lead_id,tag, operator, 'trigger_date_definition', trigger_date_def)
    db.print_record(operator, f"{operator} - UPDATE ",rec)
    return {"statusCode":200, "body": json.dumps({"message" : f"Record deleted from {operator}"})}

def fetch_zap_codes(event,context):
    s3.download_file(os.environ['BUCKET'], 'config/scheduler.conf', '/tmp/scheduler.conf')
    config = configparser.ConfigParser()
    config.read('/tmp/scheduler.conf')
    zap_codes =  [{'id': key, 'key':key} for key in config['urls']]
    return {"statusCode": 200, "body": json.dumps(zap_codes)}
     