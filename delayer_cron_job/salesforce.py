import requests
import os
import json
import csv
import boto3
s3 = boto3.client('s3')
import configparser

#Object to get auth token from salesforce and send a query to get all
#the necessary fields for leads whose reminder's status has to be updated
class Salesforce:
    # everything comes from dockerfile
    def __init__(self, config, token=''):
        self.auth_url = config.get('salesforce','AUTH_URL')
        self.query_url = config.get('salesforce','QUERY_URL')
        self.get_object_fields_url = config.get('salesforce','OBJECT_FIELDS_URL')
        self.client_id = config.get('salesforce','CLIET_ID')
        self.client_secret = config.get('salesforce','CLIENT_SECRET')
        self.password = config.get('salesforce','PASSWORD')
        self.username = config.get('salesforce','USERNAME')
        self.config = config
        #this is for my convenience
        if token != '':
            self.token = token

    #send requst to salesforce to get auth token and store it in the object
    # this will be invoked each time that the container is spawned (every hour or so)
    def authenticate(self):
        if hasattr(self,'token'):
            return self.token
        parameters = {
            'grant_type' : 'password',
            'client_id' : self.client_id,
            'client_secret' : self.client_secret,
            'username' : self.username,
            'password':self.password
        }
        resp = requests.post(self.auth_url, params=parameters)
        body = resp.json()
        self.token = body["access_token"]
        return body["access_token"]


    # send the query to fetch fields found above from objects with lead ids
    # fetched from the db
    def get_records(self, lead_ids):
        fields = ['ON_HOLD__c', 'PRECON_DATE__c', 'PREDEMO_DATE__c']
        fields_string = ",".join(fields)
        ids_arr_formatted = list(map(lambda x: "\'" + x + "\'" ,lead_ids))
        ids_string = ",".join(ids_arr_formatted )
        query = f"SELECT Id,Name,{fields_string} FROM Lead WHERE Id IN ({ids_string})"
        r = requests.get(self.query_url,params={'q':query}, headers={'Authorization':f"Bearer {self.token}"})
        body = r.json()
        if type(body) is list:
            raise Exception(f"Error from salesforce: {body[0]['message']}")
        body = r.json()['records']
        for rec in body:
            del rec['attributes']
        return body
        

