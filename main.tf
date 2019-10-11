# --------------------------------
# Creates cloud resources in AWS
# --------------------------------
provider "aws" {}

variable "image_bucket" {
    description = "The AWS S3 bucket for the uploaded images, and for the current working image"
    type        = "string"
}

variable "website_bucket" {
    description = "The AWS S3 bucket to host the statistics website"
    type        = "string"
}

variable "stats_table" {
    description = "The AWS DynamoDB table name for stats"
    type        = "string"
}

variable "stats_key" {
    description = "The AWS DynamoDB table primary key for stats"
    type        = "string"
}

variable "trend_table" {
    description = "The AWS DynamoDB table name for trend data"
    type        = "string"
}

variable "trend_key" {
    description = "The AWS DynamoDB table primary key for trend data"
    type        = "string"
}

resource "aws_s3_bucket" b1 {
  bucket = var.image_bucket
  acl    = "private"
}

resource "aws_dynamodb_table" t1 {
  name           = var.stats_table
  read_capacity  = 5
  write_capacity = 5
  hash_key       = var.stats_key
  attribute {
    name = var.stats_key
    type = "S"
  }
}

resource "aws_dynamodb_table" t2 {
  name           = var.trend_table
  read_capacity  = 5
  write_capacity = 5
  hash_key       = var.trend_key
  attribute {
    name = var.trend_key
    type = "S"
  }
}