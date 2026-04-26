# Lab 3: Automated Cost Optimization (Lifecycle Policies)

**Goal:** Automate storage tiering. Application logs shouldn't sit in expensive standard storage forever. We will configure a rule to transition logs to Glacier after 30 days.
```bash
# 1. Create the correctly formatted lifecycle policy JSON
cat <<EOF > lifecycle.json
{
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
EOF

# 2. Apply the lifecycle policy to the primary bucket
awslocal s3api put-bucket-lifecycle-configuration \
  --bucket my-company-data \
  --lifecycle-configuration file://lifecycle.json
aws s3api put-bucket-lifecycle-configuration \
  --bucket my-company-data \
  --lifecycle-configuration file://lifecycle.json
```

## 🧠 Key Concepts & Importance

- **S3 Lifecycle Management:** Allows you to manage your objects so that they are stored cost-effectively throughout their lifecycle.
- **Lifecycle Rules:** A set of operations applied to a group of objects. There are two types of actions:
    - **Transition Actions:** Define when objects transition to another storage class (e.g., Standard to Glacier).
    - **Expiration Actions:** Define when objects expire and are deleted.
- **S3 Glacier:** A secure, durable, and extremely low-cost storage class for data archiving and long-term backup.
- **Prefix Filtering:** Allows you to apply rules to a subset of objects in your bucket (e.g., everything in the `logs/` "folder").
- **Cost Optimization:** By automatically moving infrequently accessed data to cheaper storage tiers, you can significantly reduce your AWS bill.

## 🛠️ Command Reference

- `s3api put-bucket-lifecycle-configuration`: Creates a new lifecycle configuration for the bucket or replaces an existing lifecycle configuration.
    - `--bucket`: The name of the bucket.
    - `--lifecycle-configuration`: The JSON document defining the lifecycle rules.

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
