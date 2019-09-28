import boto3
import storage

client = boto3.client('rekognition')


def detect(ct):
    # Step 1. Are there faces in the image?
    if detect_faces(ct):
        # Step 2. Is the picture of a celebrity?
        recognize_celebrities()
    # Step 3. What else is in the picture?
    detect_labels(ct)
    # Step 4. Are there words?
    detect_text(ct)


def detect_faces(ct) -> bool:
    # img - name of image on disk
    # ct  - confidence threshold for API
    print("looking for a face...")
    print(storage.bucket)
    result = client.detect_faces(
        Image=dict(S3Object={'Bucket': storage.bucket, 'Name': storage.key}),
        Attributes=['ALL'])
    faces = result['FaceDetails']
    if faces:
        print("faces found:", len(faces))
        for face in faces:
            check_str(face, 'Gender', ct)
            ages = face['AgeRange']
            print("between the ages of", ages['Low'], "and", ages['High'])
            check_bool(face, 'Smile', 'smiling', ct)
            check_bool(face, 'Eyeglasses', 'wearing eyeglasses', ct)
            check_bool(face, 'Sunglasses', 'wearing sunglasses', ct)
            check_bool(face, 'Beard', 'has a beard', ct)
            check_bool(face, 'Mustache', 'has a mustache', ct)
            check_bool(face, 'EyesOpen', 'eyes are open', ct)
            check_bool(face, 'MouthOpen', 'mouth is open', ct)
            emotions = face['Emotions']
            if emotions:
                print('feeling...')
                for emotion in emotions:
                    if emotion['Confidence'] > ct:
                        print(emotion['Type'].lower())
        return True
    return False


def recognize_celebrities():
    print("checking for celebrity...")
    result = client.recognize_celebrities(
        Image=dict(S3Object={'Bucket': storage.bucket, 'Name': storage.key}))
    for celebrity in result['CelebrityFaces']:
        print("Name: {} [{}%]".format(celebrity['Name'], celebrity['MatchConfidence']))
        # TODO: scrape the URL for IMDB data


def detect_labels(ct):
    print('detecting labels...')
    result = client.detect_labels(
        Image=dict(S3Object={'Bucket': storage.bucket, 'Name': storage.key}))
    labels = result['Labels']
    for label in labels:
        if label['Confidence'] >= ct:
            print(label['Name'])


def detect_text(ct):
    print('detecting text...')
    result = client.detect_text(
        Image=dict(S3Object={'Bucket': storage.bucket, 'Name': storage.key}))
    detections = result['TextDetections']
    for text in detections:
        if text['Type'] == 'LINE' and text['Confidence'] > ct:
            print(text['DetectedText'])


# Check String Attribute
def check_str(struct, attr, ct):
    attribute = struct[attr]
    if attribute['Confidence'] > ct:
        print(attribute['Value'].lower())


# Check Boolean Attribute
def check_bool(struct, attr, msg, ct):
    attribute = struct[attr]
    if attribute['Value'] and attribute['Confidence'] > ct:
        print(msg)
