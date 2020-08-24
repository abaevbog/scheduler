import boto3
import time
import pytz
from datetime import datetime
client = boto3.client('logs')


class Log():
    def __init__(self):
        self.stream_names = {}
        self.sequence_token = None
        self.called = False
        print("Inited log")

    def create_stream(self,prefix):
        print("creating stream")
        now = datetime.now(pytz.timezone('America/New_York')).strftime("%Y-%m-%d %H:%M:%S").replace(' ','-').replace(':','-')
        response = client.create_log_stream(
            logGroupName='scheduler',
            logStreamName=f"scheduler/{prefix}/{now}"
        )
        print("Created stream")
        self.stream_names[prefix] = f"scheduler/{prefix}/{now}"

    def send_to_cloudwatch(self, prefix, log):
        print("Sending to cloudwatch")
        if self.stream_names.get(prefix) is None:
            self.create_stream(prefix)
        inputs = {
                'logGroupName':'scheduler',
                'logStreamName': self.stream_names[prefix],
                'logEvents':[
                    {
                        'timestamp': int(time.time()*1000),
                        'message': log
                    },
                ],
                'sequenceToken':self.sequence_token
            }
        if inputs.get('sequenceToken') is None:
            del inputs['sequenceToken']
        response = client.put_log_events(**inputs)
        print("Sent")
        self.sequence_token = response['nextSequenceToken']

