# Lab 7: Disaster Recovery (Cross-Region Replication)

**Goal:** Protect mission-critical data by automatically replicating all objects uploaded to the primary bucket (`us-east-1`) to a backup bucket in Europe (`eu-west-1`).
```bash
# 1. Create a destination bucket in a different region (eu-west-1)
awslocal s3api create-bucket \
  --bucket dr-backup-bucket \
  --region eu-west-1 \
  --create-bucket-configuration LocationConstraint=eu-west-1
aws s3api create-bucket \
  --bucket dr-backup-bucket \
  --region eu-west-1 \
  --create-bucket-configuration LocationConstraint=eu-west-1

# 2. Enable versioning on destination bucket (Required for CRR)
awslocal s3api put-bucket-versioning \
  --bucket dr-backup-bucket \
  --versioning-configuration Status=Enabled
aws s3api put-bucket-versioning \
  --bucket dr-backup-bucket \
  --versioning-configuration Status=Enabled

# 3. Create an IAM Role for replication (Trust policy)
cat <<EOF > crr-role.json
{
  "Version": "2012-10-17",
  "Statement": [{"Effect": "Allow", "Principal": {"Service": "s3.amazonaws.com"}, "Action": "sts:AssumeRole"}]
}
EOF
ROLE_ARN=$(awslocal iam create-role --role-name S3ReplicationRole --assume-role-policy-document file://crr-role.json --query 'Role.Arn' --output text)
ROLE_ARN=$(aws iam create-role --role-name S3ReplicationRole --assume-role-policy-document file://crr-role.json --query 'Role.Arn' --output text)

# 4. Apply the Replication rule to the source bucket
cat <<EOF > replication.json
{
  "Role": "$ROLE_ARN",
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
EOF

awslocal s3api put-bucket-replication \
  --bucket my-company-data \
  --replication-configuration file://replication.json
aws s3api put-bucket-replication \
  --bucket my-company-data \
  --replication-configuration file://replication.json
```

## 🧠 Key Concepts & Importance

- **Cross-Region Replication (CRR):** Automatically replicates data across AWS Regions. It provides high availability and disaster recovery by ensuring that a copy of your data exists in a geographically distant location.
- **Versioning Requirement:** Versioning must be enabled on both the source and destination buckets for replication to work.
- **IAM Role for Replication:** S3 requires an IAM role with permissions to read objects from the source bucket and replicate them to the destination bucket.
- **Compliance & Data Sovereignty:** CRR helps meet compliance requirements that mandate data be stored at a specific distance from the primary location.
- **Reduced Latency:** Replicating data to a region closer to your international users can also improve download speeds for those users.

## 🛠️ Command Reference

- `s3api create-bucket`: Creates a new S3 bucket in a specific region.
    - `--region`: Specifies the AWS region.
    - `--create-bucket-configuration`: Required for regions outside of `us-east-1`.
- `s3api put-bucket-versioning`: Enables versioning (mandatory for CRR).
- `iam create-role`: Creates the service role that S3 will assume to perform replication.
- `s3api put-bucket-replication`: Applies the replication configuration to the source bucket.
    - `--replication-configuration`: The JSON defining rules, destination bucket, and IAM role.

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
