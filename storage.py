import boto3
import uuid

s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')

key = 'image'
# repeated in main.tf
archive_dir = 'img'
bucket = 'lnrs-alpharetta'


def upload(img):
    print("uploading image to S3...")
    s3_client.upload_file(Filename=img, Bucket=bucket, Key=key)


def delete():
    s3_client.delete_object(Bucket=bucket, Key=key)


def archive():
    print("archiving image...")
    filename = str(uuid.uuid4())
    s3_resource.Object(bucket_name=bucket, key='{}/{}'.format(archive_dir, filename)).copy_from(
        CopySource='{}/{}'.format(bucket, key))
    delete()
    print("archive complete")
