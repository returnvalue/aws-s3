# Lab 5: Secure Third-Party Access (Pre-signed URLs)

**Goal:** A vendor needs to download the `report.txt` file from Lab 1, but they don't have AWS credentials. Generate a time-limited Pre-signed URL.
```bash
# Generate a secure pre-signed URL valid for exactly 1 hour (3600 seconds)
awslocal s3 presign s3://my-company-data/report.txt --expires-in 3600
aws s3 presign s3://my-company-data/report.txt --expires-in 3600

# (In real AWS, you would email this long URL string to the vendor. 
# Once the hour passes, the link permanently expires).
```

## 🧠 Key Concepts & Importance

- **Pre-signed URLs:** A URL that you can provide to your users to grant temporary access to a specific S3 object. With a pre-signed URL, you can let your users upload or download objects to your S3 bucket without requiring them to have AWS security credentials or permissions.
- **Time-Limited Access:** Pre-signed URLs have an expiration time that you set. Access is automatically revoked once the time limit is reached.
- **Security:** Because the URL is signed with your credentials, it carries your permissions. However, the scope is limited to the specific object and action (GET/PUT) defined when the URL was generated.
- **Use Cases:** 
    - Providing temporary access to private files (e.g., invoices, reports).
    - Allowing users to upload files directly to S3 from a web browser without exposing your backend credentials.
    - Sharing data with third-party vendors for a specific window of time.

## 🛠️ Command Reference

- `s3 presign`: Generates a pre-signed URL for an Amazon S3 object.
    - `s3://bucket/key`: The S3 URI of the object.
    - `--expires-in`: The number of seconds until the pre-signed URL expires (default is 3600 seconds).

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
