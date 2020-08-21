import boto3
client = boto3.client('logs')

response = client.put_log_events(
    logGroupName='scheduler',
    logStreamName='scheduler/reminder/914cb92a-d2e6-4520-8cd9-7ba7da7cf5d5',
    logEvents=[
        {
            'timestamp': 1598017202853,
            'message': 'test - test bububu'
        },
    ],
    sequenceToken='49604816566499503976597295438267463966411715612747618946'
)
print(response)