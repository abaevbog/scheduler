import sys
sys.path.append('/Users/bogdanabaev/RandomProgramming/BasementRemodeling/scheduler/scheduler/delayer')
sys.path.append('/Users/bogdanabaev/RandomProgramming/BasementRemodeling/scheduler/scheduler/')
from salesforce import Salesforce
import unittest
from delayer import Delayer
import boto3
import configparser
from entries import Dummy
import pytz
from datetime import datetime, timedelta
      
config = configparser.ConfigParser()
with open(r'scheduler.conf') as f:
    config.read_file(f)
salesforce = Salesforce(config)
database = Delayer(config)
token = salesforce.authenticate()
database.get_salesforce_data()