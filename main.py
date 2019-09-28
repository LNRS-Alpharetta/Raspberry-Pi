import rekognition
import storage

while True:
    # speaker will emit a ready signal when the system is initialized
    # object is triggered by a mechanical action - button push
    # speaker emits a countdown
    # capture picture from camera
    # save picture to /tmp/image.jpg
    # upload picture to S3
    # storage.upload("./img/image.png")
    # delete /tmp/image.jpg
    # call rekognition apis [faces][celebs][labels][text]
    rekognition.detect(90)
    # archive working file in bucket root
    storage.archive()
    # store labels and counts to DynamoDB
    #   JavaScript generated on stats
    #   website updated with graph and photo booth
    # speaker emits voice of what is analyzed
    break
