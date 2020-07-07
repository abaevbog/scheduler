import psycopg2
import os 
import pytz
import sys
from datetime import datetime
from random import randint
from scheduler_db import Scheduler
print(sys.path)
from delayer_db import Delayer

class Database():
    def __init__(self, config):
        print("Initing DB")
        print(config)
        conn = psycopg2.connect(
            database = config.get('database'),
            user = config.get('user'), 
            password = config.get('password'), 
            host = config.get('host'), 
            port = config.get('port')
        )
        self.connection = conn
        self.cursor = conn.cursor()
        self.config = config
        self.scheduler = Scheduler(conn,self.cursor)
        self.delayer = Delayer(conn,self.cursor)
        print("DN connected")

    def create_tables(self):
        self.scheduler.create_reminders_table()
        self.scheduler.create_salesforce_recs_table()
        self.delayer.create_delayer_table()