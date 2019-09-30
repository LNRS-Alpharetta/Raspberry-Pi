import boto3
import storage

client = boto3.client('rekognition')


def detect_faces(ct) -> []:
    # ct  - confidence threshold for API
    # returns a list of faces found, includes all attributes found
    # appends the word 'face' as a delimiter
    # example: ['face','male','age 23-35','face','female','age 35-45]']
    labels = []
    print("looking for a face...")
    result = client.detect_faces(
        Image=dict(S3Object={'Bucket': storage.bucket, 'Name': storage.key}),
        Attributes=['ALL'])
    faces = result['FaceDetails']
    if faces:
        for face in faces:
            labels.append('face')
            check_str(labels, face, 'Gender', ct)
            ages = face['AgeRange']
            labels.append("age {}-{}".format(ages['Low'], ages['High']))
            check_bool(labels, face, 'Smile', ct)
            check_bool(labels, face, 'Eyeglasses', ct)
            check_bool(labels, face, 'Sunglasses', ct)
            check_bool(labels, face, 'Beard', ct)
            check_bool(labels, face, 'Mustache', ct)
            check_bool(labels, face, 'EyesOpen', ct)
            check_bool(labels, face, 'MouthOpen', ct)
            emotions = face['Emotions']
            if emotions:
                for emotion in emotions:
                    if emotion['Confidence'] > ct:
                        labels.append(emotion['Type'].lower())
    print(labels)
    return labels


def recognize_celebrities() -> []:
    # returns a list of celebrities found, includes confidence score and any Urls
    # appends the word 'celebrity' as a delimiter
    # example: ['celebrity','John Lennon',95.0,'celebrity','George Harrison', 87.0]
    labels = []
    print("checking for celebrity...")
    result = client.recognize_celebrities(
        Image=dict(S3Object={'Bucket': storage.bucket, 'Name': storage.key}))
    celebrities = result['CelebrityFaces']
    if celebrities:
        for celebrity in celebrities:
            labels.append('celebrity')
            labels.append(celebrity['Name'])
            labels.append(celebrity['MatchConfidence'])
            for url in celebrity['Urls']:
                labels.append(url)
    print(labels)
    return labels


def detect_labels(ct) -> []:
    # returns a list of labels found over the given confidence threshold
    # example: ['Person','Human','Shoe']
    labels = []
    print('detecting labels...')
    result = client.detect_labels(
        Image=dict(S3Object={'Bucket': storage.bucket, 'Name': storage.key}))
    for label in result['Labels']:
        if label['Confidence'] >= ct:
            labels.append(label['Name'])
    print(labels)
    return labels


def detect_text(ct) -> []:
    # detects text and returns if over the given confidence threshold
    lines = []
    print('detecting text...')
    result = client.detect_text(
        Image=dict(S3Object={'Bucket': storage.bucket, 'Name': storage.key}))
    for text in result['TextDetections']:
        if (text['Type'] == 'LINE' or text['Type'] == 'WORD') and text['Confidence'] > ct:
            lines.append(text['DetectedText'])
    print(lines)
    return lines


# Check String Attribute
def check_str(labels, struct, attr, ct):
    attribute = struct[attr]
    if attribute['Confidence'] > ct:
        labels.append(attribute['Value'].lower())


# Check Boolean Attribute
def check_bool(labels, struct, attr, ct):
    attribute = struct[attr]
    if attribute['Value'] and attribute['Confidence'] > ct:
        labels.append(attr)
