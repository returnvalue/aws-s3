# Lab 6: Content Delivery & Edge Caching (CloudFront Origin)

**Goal:** Serve a static website stored in S3 to global users with minimal latency by fronting it with Amazon CloudFront.
```bash
# 1. Create a bucket for static web hosting
awslocal s3api create-bucket --bucket static-web-bucket
aws s3api create-bucket --bucket static-web-bucket

# 2. Upload an index.html file
echo '<html><body><h1>Hello from the CloudFront Edge!</h1></body></html>' > index.html
awslocal s3api put-object \
  --bucket static-web-bucket \
  --key index.html \
  --body index.html \
  --content-type "text/html"
aws s3api put-object \
  --bucket static-web-bucket \
  --key index.html \
  --body index.html \
  --content-type "text/html"

# 3. Create a CloudFront Distribution pointing to the S3 bucket as its origin
awslocal cloudfront create-distribution \
  --origin-domain-name static-web-bucket.s3.amazonaws.com \
  --default-root-object index.html
aws cloudfront create-distribution \
  --origin-domain-name static-web-bucket.s3.amazonaws.com \
  --default-root-object index.html
```

## 🧠 Key Concepts & Importance

- **Amazon CloudFront:** A fast content delivery network (CDN) service that securely delivers data, videos, applications, and APIs to customers globally with low latency and high transfer speeds.
- **Edge Locations:** CloudFront uses a global network of edge locations to cache copies of your content close to your viewers.
- **Origin:** The source of your content (in this case, an S3 bucket). CloudFront retrieves your content from the origin when it's not already in the edge cache.
- **Latency Reduction:** By serving content from edge locations, CloudFront reduces the distance data travels, significantly improving page load times for global users.
- **Static Website Hosting:** S3 can host static websites, and when combined with CloudFront, it provides a highly scalable and performant hosting solution.

## 🛠️ Command Reference

- `s3api create-bucket`: Creates a new S3 bucket.
    - `--bucket`: The name of the bucket.
- `s3api put-object`: Adds an object to a bucket.
    - `--bucket`: The destination bucket.
    - `--key`: The object name (e.g., `index.html`).
    - `--body`: The file content.
    - `--content-type`: Sets the MIME type (essential for browsers to render HTML).
- `cloudfront create-distribution`: Creates a new web distribution.
    - `--origin-domain-name`: The DNS domain name of the S3 bucket or HTTP server from which CloudFront gets your files.
    - `--default-root-object`: The object that CloudFront returns when a viewer requests the root URL (e.g., `index.html`).

---

💡 **Pro Tip: Using `aws` instead of `awslocal`**

If you prefer using the standard `aws` CLI without the `awslocal` wrapper or repeating the `--endpoint-url` flag, you can configure a dedicated profile in your AWS config files.

### 1. Configure your Profile
Add the following to your `~/.aws/config` file:
```ini
[profile localstack]
region = us-east-1
output = json
# This line redirects all commands for this profile to LocalStack
endpoint_url = http://localhost:4566
```

Add matching dummy credentials to your `~/.aws/credentials` file:
```ini
[localstack]
aws_access_key_id = test
aws_secret_access_key = test
```

### 2. Use it in your Terminal
You can now run commands in two ways:

**Option A: Pass the profile flag**
```bash
aws iam create-user --user-name DevUser --profile localstack
```

**Option B: Set an environment variable (Recommended)**
Set your profile once in your session, and all subsequent `aws` commands will automatically target LocalStack:
```bash
export AWS_PROFILE=localstack
aws iam create-user --user-name DevUser
```

### Why this works
- **Precedence**: The AWS CLI (v2) supports a global `endpoint_url` setting within a profile. When this is set, the CLI automatically redirects all API calls for that profile to your local container instead of the real AWS cloud.
- **Convenience**: This allows you to use the standard documentation commands exactly as written, which is helpful if you are copy-pasting examples from AWS labs or tutorials.
