import boto3
import json

s3api = boto3.client('s3', endpoint_url="http://localhost:4566", region_name="us-east-1")

lifecycle_config = {
    "Rules": [
        {
            "ID": "ArchiveOldLogs",
            "Filter": {
                "Prefix": "logs/"
            },
            "Status": "Enabled",
            "Transitions": [
                {
                    "Days": 30,
                    "StorageClass": "GLACIER"
                }
            ]
        }
    ]
}

with open('lifecycle.json', 'w') as f:
    json.dump(lifecycle_config, f)

s3api.put_bucket_lifecycle_configuration(
    Bucket='my-company-data',
    LifecycleConfiguration=lifecycle_config
)
