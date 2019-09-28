import boto3

s3 = boto3.client('s3')

bucket = 'lnrs-alpharetta'
key = 'image.png'


def upload(img):
    print("uploading image to S3...")
    s3.upload_file(Filename=img, Bucket=bucket, Key=key)
    print("upload complete")


def delete():
    print("cleaning up")
    s3.delete_object(Bucket=bucket, Key=key)


def archive():
    print("archiving image...")
    # move or rename
    # s3.upload_file(Filename=img, Bucket=bucket, Key=key)
    print("upload complete")