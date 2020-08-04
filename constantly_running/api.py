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
#print(config)
#db = Database(config)
#print("DB DONE")


def create_tables(event,context):
    print("Creating tables")
    #db.create_tables()
    return {"statusCode":200, "body": json.dumps({"message" : "Tables created!"})}


def fetch_zap_codes(event,context):
    s3.download_file(os.environ['BUCKET'], 'config/scheduler.conf', '/tmp/scheduler.conf')
    config = configparser.ConfigParser()
    config.read('/tmp/scheduler.conf')
    zap_codes =  [{'id': key, 'key':key} for key in config['urls']]
    return {"statusCode": 200, "body": json.dumps(zap_codes)}
     