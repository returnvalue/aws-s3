import boto3

s3api = boto3.client('s3', endpoint_url="http://localhost:4566", region_name="us-east-1")
cloudfront = boto3.client('cloudfront', endpoint_url="http://localhost:4566", region_name="us-east-1")

s3api.create_bucket(Bucket='static-web-bucket')

with open('index.html', 'w') as f:
    f.write('<html><body><h1>Hello from the CloudFront Edge!</h1></body></html>\n')

s3api.put_object(
    Bucket='static-web-bucket',
    Key='index.html',
    Body=open('index.html', 'rb'),
    ContentType='text/html'
)

cloudfront.create_distribution(
    DistributionConfig={
        'CallerReference': 'my-distribution',
        'Origins': {
            'Quantity': 1,
            'Items': [
                {
                    'Id': 'my-origin',
                    'DomainName': 'static-web-bucket.s3.amazonaws.com',
                    'S3OriginConfig': {
                        'OriginAccessIdentity': ''
                    }
                }
            ]
        },
        'DefaultCacheBehavior': {
            'TargetOriginId': 'my-origin',
            'ViewerProtocolPolicy': 'allow-all',
            'MinTTL': 0,
            'ForwardedValues': {
                'QueryString': False,
                'Cookies': {'Forward': 'none'}
            }
        },
        'Comment': '',
        'Enabled': True,
        'DefaultRootObject': 'index.html'
    }
)
