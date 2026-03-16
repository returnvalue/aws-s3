import boto3
import json

sqs = boto3.client('sqs', endpoint_url="http://localhost:4566", region_name="us-east-1")
s3api = boto3.client('s3', endpoint_url="http://localhost:4566", region_name="us-east-1")

queue_response = sqs.create_queue(QueueName='S3EventQueue')
queue_url = queue_response['QueueUrl']

attrs_response = sqs.get_queue_attributes(QueueUrl=queue_url, AttributeNames=['QueueArn'])
queue_arn = attrs_response['Attributes']['QueueArn']

notification_config = {
    "QueueConfigurations": [
        {
            "QueueArn": queue_arn,
            "Events": ["s3:ObjectCreated:*"]
        }
    ]
}

with open('notification.json', 'w') as f:
    json.dump(notification_config, f)

s3api.put_bucket_notification_configuration(
    Bucket='my-company-data',
    NotificationConfiguration=notification_config
)

with open('new-log.txt', 'w') as f:
    f.write('New application log entry\n')

s3api.put_object(Bucket='my-company-data', Key='logs/new-log.txt', Body=open('new-log.txt', 'rb'))

sqs.receive_message(QueueUrl=queue_url)
