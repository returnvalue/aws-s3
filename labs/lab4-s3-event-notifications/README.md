# Lab 4: Event-Driven Architectures (S3 Event Notifications to SQS)

**Goal:** Decouple your architecture. Whenever a new log file is uploaded to the bucket, automatically send an event notification to an SQS queue so a downstream service can process it.
```bash
# 1. Create an SQS Queue and get its ARN
QUEUE_URL=$(awslocal sqs create-queue --queue-name S3EventQueue --query 'QueueUrl' --output text)
QUEUE_URL=$(aws sqs create-queue --queue-name S3EventQueue --query 'QueueUrl' --output text)
QUEUE_ARN=$(awslocal sqs get-queue-attributes --queue-url $QUEUE_URL --attribute-names QueueArn --query 'Attributes.QueueArn' --output text)
QUEUE_ARN=$(aws sqs get-queue-attributes --queue-url $QUEUE_URL --attribute-names QueueArn --query 'Attributes.QueueArn' --output text)

# 2. Configure S3 to send ObjectCreated events to the SQS queue
cat <<EOF > notification.json
{
  "QueueConfigurations": [
    {
      "QueueArn": "$QUEUE_ARN",
      "Events": ["s3:ObjectCreated:*"]
    }
  ]
}
EOF

awslocal s3api put-bucket-notification-configuration \
  --bucket my-company-data \
  --notification-configuration file://notification.json
aws s3api put-bucket-notification-configuration \
  --bucket my-company-data \
  --notification-configuration file://notification.json

# 3. Upload a file to trigger the event
echo "New application log entry" > new-log.txt
awslocal s3api put-object --bucket my-company-data --key logs/new-log.txt --body new-log.txt
aws s3api put-object --bucket my-company-data --key logs/new-log.txt --body new-log.txt

# 4. Read the message from the SQS queue (You will see the S3 JSON event payload)
awslocal sqs receive-message --queue-url $QUEUE_URL
aws sqs receive-message --queue-url $QUEUE_URL
```

## 🧠 Key Concepts & Importance

- **Event-Driven Architecture:** A design pattern where actions (events) in one part of the system trigger actions in another, without direct dependencies.
- **S3 Event Notifications:** A feature that allows you to receive notifications when certain events happen in your S3 bucket, such as object creation, deletion, or restoration.
- **Amazon SQS (Simple Queue Service):** A fully managed message queuing service that enables you to decouple and scale microservices, distributed systems, and serverless applications.
- **Decoupling:** Reducing direct connections between system components so that changes or failures in one don't directly affect others.
- **Asynchronous Processing:** Allowing tasks to be performed in the background, improving system performance and responsiveness.

## 🛠️ Command Reference

- `sqs create-queue`: Creates a new SQS queue.
    - `--queue-name`: The name of the new queue.
- `sqs get-queue-attributes`: Gets the attributes of an SQS queue.
    - `--queue-url`: The URL of the queue.
    - `--attribute-names`: The attributes to retrieve (e.g., `QueueArn`).
- `s3api put-bucket-notification-configuration`: Configures notifications for an S3 bucket.
    - `--bucket`: The name of the bucket.
    - `--notification-configuration`: The JSON defining the event rules and destinations.
- `sqs receive-message`: Retrieves one or more messages from the specified queue.
    - `--queue-url`: The URL of the queue to receive messages from.

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
