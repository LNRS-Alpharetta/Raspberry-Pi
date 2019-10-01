# --------------------------------
# Creates cloud resources in AWS
# --------------------------------
provider "aws" {}

resource "aws_s3_bucket" "lnrs-alpharetta" {
  bucket = "lnrs-alpharetta"
  acl    = "private"
}

resource "aws_s3_bucket_object" "lnrs-alpharetta-img" {
    bucket     = "lnrs-alpharetta"
    acl        = "private"
    key        = "img/"
    source     = "/dev/null"
    depends_on = [aws_s3_bucket.lnrs-alpharetta]
}

resource "aws_dynamodb_table" "raspberry-pi-camera" {
  name           = "raspberry-pi-camera"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "label"
  attribute {
    name = "label"
    type = "S"
  }
}