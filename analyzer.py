import os
import gzip
import json
import base64
from datetime import datetime
import boto3
def handler(event, context):
  
    SNS_TOPIC = os.environ.get("SNS_TOPIC", None)
    if SNS_TOPIC is None:
      print("no SNS topic in environment.  Exit")
      exit(1)
    
    print(event)
    try:
        logData = str(
            gzip.decompress(base64.b64decode(
                event["awslogs"]["data"])), "utf-8"
        )
    except Exception as error:
        logging.error("failed to retrieve message data: %s", error)
        return 500

    jsonBody = json.loads(logData)
    print(jsonBody)

    print(f"Account: {jsonBody['owner']}")
    print(f"Source LogGroup: {jsonBody['logGroup']}")
    print(f"Source LogStream: {jsonBody['logStream']}")

    for filterData in jsonBody["subscriptionFilters"]:
        print(f"Subscription Filter: {filterData}")

    print(f"Message Type: {jsonBody['messageType']}")

    for logEvent in jsonBody["logEvents"]:
        print(f"logEvent = {logEvent}")
        print(f"event ID {logEvent['id']} at {datetime.fromtimestamp(logEvent['timestamp'] / 1000.0)}")

        snd = logEvent.get('message','')
        if snd == '':
          exit(0)
        print(f"message is {snd}")
        
        sns_client = boto3.client('sns')
        response = sns_client.publish(
          TopicArn=SNS_TOPIC,
          Message=snd,
          Subject='FAIL detected',
          )
        print(f"sns response = {response}")

        exit(0)