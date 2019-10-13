import boto3
import vars
import uuid

s3 = boto3.client('s3')

bucket = vars.get("image_bucket")


def upload(img) -> {}:
    key = "{}.{}".format(str(uuid.uuid4()), 'jpg')
    s3.upload_file(Filename=img, Bucket=bucket, Key=key)
    return dict(S3Object={'Bucket': bucket, 'Name': key})


def delete(key):
    s3.delete_object(Bucket=bucket, Key=key)
