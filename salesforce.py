import requests
import os
import json


#Object to get auth token from salesforce and send a query to get all
#the necessary fields for leads whose reminder's status has to be updated
class Salesforce:
    # everything comes from dockerfile
    def __init__(self, token=''):
        self.auth_url = os.environ['AUTH_URL']
        self.query_url = os.environ['QUERY_URL']
        self.get_object_fields_url = os.environ['OBJECT_FIELDS_URL']
        self.client_id = os.environ['CLIET_ID']
        self.client_secret = os.environ['CLIENT_SECRET']
        self.password = os.environ['PASSWORD']
        self.username = os.environ['USERNAME']
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
        checkbox_fields = [i["name"] for i in body["fields"] if i["type"] == "boolean"]
        date_fields = [i["name"] for i in body["fields"] if "DATE" in i["name"]]
        fields = list(set(checkbox_fields + date_fields ))
        return fields

    #send the query to fecth all fields from above from objects with lead ids provided
    def query(self, lead_ids, fields):
        fields_string = ",".join(fields)
        ids_string = ",".join(lead_ids)
        query = f"SELECT Id,Name,{fields_string} FROM Lead WHERE Id IN ('{ids_string}')"
        r = requests.get(self.query_url,params={'q':query}, headers={'Authorization':f"Bearer {self.token}"})
        body = r.json()
        return body