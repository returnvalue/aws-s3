# Lab 1: Foundational S3 & Data Protection (Versioning)

**Goal:** Create a core storage bucket and enable versioning to protect against accidental overwrites.
```bash
# 1. Create the primary production bucket
awslocal s3api create-bucket --bucket my-company-data --region us-east-1
aws s3api create-bucket --bucket my-company-data --region us-east-1

# 2. Enable Bucket Versioning
awslocal s3api put-bucket-versioning \
  --bucket my-company-data \
  --versioning-configuration Status=Enabled
aws s3api put-bucket-versioning \
  --bucket my-company-data \
  --versioning-configuration Status=Enabled

# 3. Create a test file and upload the first version
echo "Report Data: Version 1" > report.txt
awslocal s3api put-object --bucket my-company-data --key report.txt --body report.txt
aws s3api put-object --bucket my-company-data --key report.txt --body report.txt

# 4. Overwrite the file to simulate an update or accident
echo "Report Data: Version 2" > report.txt
awslocal s3api put-object --bucket my-company-data --key report.txt --body report.txt
aws s3api put-object --bucket my-company-data --key report.txt --body report.txt

# 5. List the object versions (You will see both versions retained!)
awslocal s3api list-object-versions --bucket my-company-data --prefix report.txt
aws s3api list-object-versions --bucket my-company-data --prefix report.txt
```

## 🧠 Key Concepts & Importance

- **S3 Bucket:** A container for objects stored in Amazon S3. Every object is contained in a bucket.
- **Bucket Versioning:** A means of keeping multiple variants of an object in the same bucket. You can use versioning to preserve, retrieve, and restore every version of every object stored in your Amazon S3 bucket.
- **Data Protection:** Versioning provides an extra layer of protection by allowing you to recover from both unintended user actions and application failures.
- **Object Key:** The unique identifier for an object within a bucket.
- **Version ID:** When you enable versioning, S3 generates a unique version ID for every object added to the bucket.

## 🛠️ Command Reference

- `s3api create-bucket`: Creates a new S3 bucket.
    - `--bucket`: The name of the bucket to create.
    - `--region`: The region where the bucket will be created.
- `s3api put-bucket-versioning`: Sets the versioning state of an existing bucket.
    - `--bucket`: The name of the bucket.
    - `--versioning-configuration`: Specifies the versioning state (e.g., `Status=Enabled`).
- `s3api put-object`: Adds an object to a bucket.
    - `--bucket`: The bucket to add the object to.
    - `--key`: The name of the object.
    - `--body`: The file to upload.
- `s3api list-object-versions`: Lists metadata about all versions of the objects in a bucket.
    - `--bucket`: The bucket name.
    - `--prefix`: Limits the response to keys that begin with the specified prefix.

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
