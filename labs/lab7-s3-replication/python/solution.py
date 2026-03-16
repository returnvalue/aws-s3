import boto3
import json

s3api = boto3.client('s3', endpoint_url="http://localhost:4566", region_name="eu-west-1")
iam = boto3.client('iam', endpoint_url="http://localhost:4566", region_name="us-east-1")
s3api_us = boto3.client('s3', endpoint_url="http://localhost:4566", region_name="us-east-1")

s3api.create_bucket(
    Bucket='dr-backup-bucket',
    CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'}
)

s3api.put_bucket_versioning(
    Bucket='dr-backup-bucket',
    VersioningConfiguration={'Status': 'Enabled'}
)

trust_policy = {
    "Version": "2012-10-17",
    "Statement": [{"Effect": "Allow", "Principal": {"Service": "s3.amazonaws.com"}, "Action": "sts:AssumeRole"}]
}

with open('crr-role.json', 'w') as f:
    json.dump(trust_policy, f)

role_response = iam.create_role(
    RoleName='S3ReplicationRole',
    AssumeRolePolicyDocument=json.dumps(trust_policy)
)
role_arn = role_response['Role']['Arn']

replication_config = {
    "Role": role_arn,
    "Rules": [
        {
            "Status": "Enabled",
            "Priority": 1,
            "DeleteMarkerReplication": { "Status": "Disabled" },
            "Filter": { "Prefix": "" },
            "Destination": {
                "Bucket": "arn:aws:s3:::dr-backup-bucket"
            }
        }
    ]
}

with open('replication.json', 'w') as f:
    json.dump(replication_config, f)

s3api_us.put_bucket_replication(
    Bucket='my-company-data',
    ReplicationConfiguration=replication_config
)
