resource "aws_kms_key" "s3_key" {
  description             = "S3 Encryption Key"
  deletion_window_in_days = 7
}

resource "aws_s3_bucket" "secure_data" {
  bucket = "secure-compliance-data"
  object_lock_enabled = true
}

resource "aws_s3_bucket_versioning" "secure_data_versioning" {
  bucket = aws_s3_bucket.secure_data.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_object" "taxes" {
  bucket     = aws_s3_bucket.secure_data.id
  key        = "taxes.txt"
  content    = "Strictly Confidential Tax Records"
  kms_key_id = aws_kms_key.s3_key.arn
  server_side_encryption = "aws:kms"
  object_lock_mode              = "COMPLIANCE"
  object_lock_retain_until_date = "2030-12-31T00:00:00Z"
}
