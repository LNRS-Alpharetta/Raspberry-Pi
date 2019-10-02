import boto3
import vars
import uuid

s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')

bucket = vars.get("image_bucket")


def upload(img) -> {}:
    key = str(uuid.uuid4())
    s3_client.upload_file(Filename=img, Bucket=bucket, Key=key)
    return dict(S3Object={'Bucket': bucket, 'Name': key})
