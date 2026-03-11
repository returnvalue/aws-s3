resource "aws_sqs_queue" "s3_event_queue" {
  name = "S3EventQueue"
}

resource "aws_s3_bucket" "my_company_data" {
  bucket = "my-company-data"
}

resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.my_company_data.id

  queue {
    queue_arn     = aws_sqs_queue.s3_event_queue.arn
    events        = ["s3:ObjectCreated:*"]
  }
}
