import boto3

kms = boto3.client('kms', endpoint_url="http://localhost:4566", region_name="us-east-1")
s3api = boto3.client('s3', endpoint_url="http://localhost:4566", region_name="us-east-1")

kms_response = kms.create_key(Description='S3 Encryption Key')
kms_key_id = kms_response['KeyMetadata']['KeyId']

s3api.create_bucket(Bucket='secure-compliance-data', ObjectLockEnabledForBucket=True)

s3api.put_bucket_versioning(
    Bucket='secure-compliance-data',
    VersioningConfiguration={'Status': 'Enabled'}
)

with open('taxes.txt', 'w') as f:
    f.write('Strictly Confidential Tax Records\n')

s3api.put_object(
    Bucket='secure-compliance-data',
    Key='taxes.txt',
    Body=open('taxes.txt', 'rb'),
    SSEKMSKeyId=kms_key_id,
    ServerSideEncryption='aws:kms',
    ObjectLockMode='COMPLIANCE',
    ObjectLockRetainUntilDate='2030-12-31T00:00:00Z'
)
