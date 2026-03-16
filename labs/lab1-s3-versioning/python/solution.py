import boto3

s3api = boto3.client('s3', endpoint_url="http://localhost:4566", region_name="us-east-1")

s3api.create_bucket(Bucket='my-company-data')

s3api.put_bucket_versioning(
    Bucket='my-company-data',
    VersioningConfiguration={'Status': 'Enabled'}
)

with open('report.txt', 'w') as f:
    f.write('Report Data: Version 1\n')

s3api.put_object(Bucket='my-company-data', Key='report.txt', Body=open('report.txt', 'rb'))

with open('report.txt', 'w') as f:
    f.write('Report Data: Version 2\n')

s3api.put_object(Bucket='my-company-data', Key='report.txt', Body=open('report.txt', 'rb'))

s3api.list_object_versions(Bucket='my-company-data', Prefix='report.txt')
