import sys
import os
sys.path.insert(1,os.getcwd() + "/db")
from database import Database
import json
import configparser
import boto3 
s3 = boto3.client('s3')

database =  os.environ['DB_NAME'],
user = os.environ['DB_USER'], 
password = os.environ['DB_PASSWORD'], 
host = os.environ['DB_HOST'], 
port = os.environ['DB_PORT']
config = {'database':database[0],'user':user[0],'password':password[0],'host':host[0],'port':port }
db = Database(config)

def create_tables(event,context):
    print("Creating tables")
    db.create_tables()
    return {"statusCode":200, "body": json.dumps({"message" : "Tables created!"})}


def fetch_zap_codes(event,context):
    with open('./tmp/scheduler.conf', 'wb') as f:
        s3.download_fileobj(os.environ['BUCKET'], 'config/scheduler.conf', f)

    config = configparser.ConfigParser()
    config.read('./tmp/scheduler.conf')
    