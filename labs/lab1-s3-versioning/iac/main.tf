resource "aws_s3_bucket" "my_company_data" {
  bucket = "my-company-data"
}

resource "aws_s3_bucket_versioning" "my_company_data_versioning" {
  bucket = aws_s3_bucket.my_company_data.id
  versioning_configuration {
    status = "Enabled"
  }
}
