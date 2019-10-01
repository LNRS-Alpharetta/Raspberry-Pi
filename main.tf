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

# Add DynamoDB