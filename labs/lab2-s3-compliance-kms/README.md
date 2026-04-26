# Lab 2: Compliance & Security (SSE-KMS & Object Lock)

**Goal:** Store highly sensitive financial data. Encrypt it using a custom KMS key and apply a "Write Once Read Many" (WORM) Object Lock in Compliance mode so it cannot be deleted by anyone (even the root user) for 5 years.
```bash
# 1. Create a Customer Managed KMS Key (CMK)
KMS_KEY_ID=$(awslocal kms create-key --description "S3 Encryption Key" --query 'KeyMetadata.KeyId' --output text)
KMS_KEY_ID=$(aws kms create-key --description "S3 Encryption Key" --query 'KeyMetadata.KeyId' --output text)
echo "Created KMS Key: $KMS_KEY_ID"

# 2. Create a new bucket specifically configured for Object Lock
awslocal s3api create-bucket \
  --bucket secure-compliance-data \
  --object-lock-enabled-for-bucket
aws s3api create-bucket \
  --bucket secure-compliance-data \
  --object-lock-enabled-for-bucket

# 3. Object Lock implicitly requires Versioning, so we enable it
awslocal s3api put-bucket-versioning \
  --bucket secure-compliance-data \
  --versioning-configuration Status=Enabled
aws s3api put-bucket-versioning \
  --bucket secure-compliance-data \
  --versioning-configuration Status=Enabled

# 4. Upload a file using SSE-KMS and enforce a COMPLIANCE Object Lock until 2030
echo "Strictly Confidential Tax Records" > taxes.txt
awslocal s3api put-object \
  --bucket secure-compliance-data \
  --key taxes.txt \
  --body taxes.txt \
  --ssekms-key-id $KMS_KEY_ID \
  --server-side-encryption aws:kms \
  --object-lock-mode COMPLIANCE \
  --object-lock-retain-until-date "2030-12-31T00:00:00Z"
aws s3api put-object \
  --bucket secure-compliance-data \
  --key taxes.txt \
  --body taxes.txt \
  --ssekms-key-id $KMS_KEY_ID \
  --server-side-encryption aws:kms \
  --object-lock-mode COMPLIANCE \
  --object-lock-retain-until-date "2030-12-31T00:00:00Z"
```

## 🧠 Key Concepts & Importance

- **SSE-KMS (Server-Side Encryption with AWS KMS):** Provides an additional layer of security by using a customer master key (CMK) stored in AWS Key Management Service (KMS) to encrypt your data. It provides audit trails for key usage.
- **S3 Object Lock:** A feature that allows you to store objects using a write-once-read-many (WORM) model. It helps prevent objects from being deleted or overwritten for a fixed amount of time or indefinitely.
- **Compliance Mode:** In compliance mode, a protected object version cannot be overwritten or deleted by any user, including the root user in your AWS account. Its retention mode cannot be changed, and its retention period cannot be shortened.
- **WORM Model:** "Write Once, Read Many" is a data storage technology that allows information to be written to a storage device once and prevents the drive from erasing or modifying the data.
- **KMS Key Management:** Using Customer Managed Keys (CMK) gives you full control over the key's lifecycle, including rotation and access policies.

## 🛠️ Command Reference

- `kms create-key`: Creates a unique customer managed KMS key in your AWS account.
    - `--description`: A description of the key.
    - `--query`: Filters the output for the KeyId.
- `s3api create-bucket`: Creates a new S3 bucket.
    - `--bucket`: The name of the bucket.
    - `--object-lock-enabled-for-bucket`: Enables S3 Object Lock for the new bucket.
- `s3api put-bucket-versioning`: Enables versioning on the bucket (required for Object Lock).
    - `--bucket`: The name of the bucket.
    - `--versioning-configuration`: Status set to `Enabled`.
- `s3api put-object`: Adds an object to a bucket with security and compliance settings.
    - `--bucket`: The destination bucket.
    - `--key`: The object name.
    - `--body`: The file content.
    - `--ssekms-key-id`: The ID of the KMS key to use for encryption.
    - `--server-side-encryption`: Specifies the encryption algorithm (`aws:kms`).
    - `--object-lock-mode`: Sets the WORM mode (`COMPLIANCE` or `GOVERNANCE`).
    - `--object-lock-retain-until-date`: The timestamp when the lock expires.

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
