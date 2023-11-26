import json

def parse_sns(s):
    """
    Takes in an SNS event, and parses out the message into a dictionary with
    all the data needed to make the reservation
    """
    message = json.loads(sns_message = event['Records'][0]['Sns']['Message'])


s = """{'Records': [{'EventSource': 'aws:sns', 'EventVersion': '1.0', 'EventSubscriptionArn': 'arn:aws:sns:us-east-1:571104494346:parking-sub:95e18092-7369-40ae-8193-176e071bd827', 'Sns': {'Type': 'Notification', 'MessageId': '3b5e067f-4b39-56df-b512-5ba6dce907a1', 'TopicArn': 'arn:aws:sns:us-east-1:571104494346:parking-sub', 'Subject': None, 'Message': '{"id": "336c50ad-a71f-4202-b16d-c9d04b66e755", "reserveOn": "2023-11-23", "reserveTarget": "2023-11-25", "reserveTime": "15:00:00.000", "resort": "SOLITUDE", "user": "e39fdf08-ee98-4c66-864a-90a6cf3543b1"}', 'Timestamp': '2023-11-23T18:10:24.547Z', 'SignatureVersion': '1', 'Signature': 'ZzmHxyT5xjhknt2QanhTB80DwwdBk9KVebQl0wwiqKgtyksiQQRVWikr2Gk68LA73VxajT6P6nejOhRF7xAkPViuUjv60iwDAvpRY+pNlncNqsDvsHwS3Ir4fjeeV6y0nbYQZ/wQdNWAvY9LOhS/Y6vxCjaJHD3ZPO2QG80+KBRhydqvmh8oOj/UkEKzIs4zvvoDvXSr8vFNbkv7U11MzgQB7Vr1S2UiQv3JGNLKdMBoGybqF4pn3GJNgGR3l0/Aoq9x76WdZZTXPwUZZ0TG7jCfW9MihP6MoYMHstLUnjpCUWEiNeCyzjcb51t4yg2ZYlpYRDM5IQHjQngn/RWoSw==', 'SigningCertUrl': 'https://sns.us-east-1.amazonaws.com/SimpleNotificationService-01d088a6f77103d0fe307c0069e40ed6.pem', 'UnsubscribeUrl': 'https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:571104494346:parking-sub:95e18092-7369-40ae-8193-176e071bd827', 'MessageAttributes': {}}}]}"""

if __name__ == "__main__":
    parse_sns(s)