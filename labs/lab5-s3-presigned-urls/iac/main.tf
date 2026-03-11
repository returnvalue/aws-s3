resource "aws_s3_bucket" "my_company_data" {
  bucket = "my-company-data"
}

resource "aws_s3_object" "report" {
  bucket = aws_s3_bucket.my_company_data.id
  key    = "report.txt"
  content = "Report Data: Version 1"
}
