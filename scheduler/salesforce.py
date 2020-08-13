import requests
import json
import boto3
s3 = boto3.client('s3')
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

    # fetch the fields of the object that we are interested in.
    # currently, we fetch all fields that have DATE (to know how soon events are)
    # and all boolean fields (to make sure we don't send requests if things have been confirmed)
    def get_object_fields(self):
        resp = requests.get(self.get_object_fields_url,headers={'Authorization':f"Bearer {self.token}"})
        body = resp.json()
        boolean_fields = [i["name"] for i in body["fields"] if i["type"] == "boolean"]
        date_fields = [i["name"] for i in body["fields"] if "DATE" in i["name"]]
        boolean_fields.sort()
        date_fields.sort()
        return boolean_fields, date_fields

    # send the query to fetch fields found above from objects with lead ids
    # fetched from the db
    def get_records(self, lead_ids, fields):
        fields.append('status')
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

    def get_classified_records(self, lead_ids, fields):
        try:
            records = self.get_records(lead_ids,fields)
        except Exception as e:
            print(f"SALESFORCE EXCEPTION: {e}")
            return []
        broken_into_satisfied_or_not = []
        keys = records[0].keys()
        for rec in records:
            print(rec)
            d = {'id':rec['Id'],'name':rec['Name'],'status':rec['Status']}
            satisfied = [key.lower() for key in rec if rec[key]]
            not_satisfied = [key.lower() for key in rec if not rec[key]]
            d['satisfied'] = satisfied
            d['not_satisfied'] = not_satisfied
            d['START_DATE'] = rec['PRECON_DATE__c']
            if rec.get('PREDEMO_DATE__c') is not None:
                d['START_DATE'] = rec['PREDEMO_DATE__c']
            broken_into_satisfied_or_not.append(d)
        return broken_into_satisfied_or_not
        

        