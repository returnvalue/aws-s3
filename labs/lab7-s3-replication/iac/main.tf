provider "aws" {
  alias  = "central"
  region = "us-east-1"
}

provider "aws" {
  alias  = "west"
  region = "eu-west-1"
}

resource "aws_s3_bucket" "source" {
  provider = aws.central
  bucket   = "my-company-data"
}

resource "aws_s3_bucket_versioning" "source" {
  provider = aws.central
  bucket   = aws_s3_bucket.source.id
  versioning_configuration { status = "Enabled" }
}

resource "aws_s3_bucket" "destination" {
  provider = aws.west
  bucket   = "dr-backup-bucket"
}

resource "aws_s3_bucket_versioning" "destination" {
  provider = aws.west
  bucket   = aws_s3_bucket.destination.id
  versioning_configuration { status = "Enabled" }
}

resource "aws_iam_role" "replication" {
  name = "S3ReplicationRole"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "s3.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_s3_bucket_replication_configuration" "replication" {
  provider = aws.central
  depends_on = [aws_s3_bucket_versioning.source]

  role   = aws_iam_role.replication.arn
  bucket = aws_s3_bucket.source.id

  rule {
    id     = "ReplicationRule"
    status = "Enabled"

    destination {
      bucket        = aws_s3_bucket.destination.arn
      storage_class = "STANDARD"
    }
  }
}
