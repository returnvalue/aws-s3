resource "aws_s3_bucket" "my_company_data" {
  bucket = "my-company-data"
}

resource "aws_s3_bucket_lifecycle_configuration" "logs_lifecycle" {
  bucket = aws_s3_bucket.my_company_data.id

  rule {
    id     = "ArchiveOldLogs"
    status = "Enabled"

    filter {
      prefix = "logs/"
    }

    transition {
      days          = 30
      storage_class = "GLACIER"
    }
  }
}
