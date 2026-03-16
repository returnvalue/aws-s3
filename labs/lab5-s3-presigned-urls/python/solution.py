import boto3

s3 = boto3.client('s3', endpoint_url="http://localhost:4566", region_name="us-east-1")

url = s3.generate_presigned_url(
    ClientMethod='get_object',
    Params={
        'Bucket': 'my-company-data',
        'Key': 'report.txt'
    },
    ExpiresIn=3600
)
