import boto3
import storage

client = boto3.client('rekognition')


def detect_faces(ct) -> []:
    # img - name of image on disk
    # ct  - confidence threshold for API
    labels = []
    print("looking for a face...")
    result = client.detect_faces(
        Image=dict(S3Object={'Bucket': storage.bucket, 'Name': storage.key}),
        Attributes=['ALL'])
    faces = result['FaceDetails']
    if faces:
        # only do the first face to keep it simple
        face = faces[0]
        check_str(labels, face, 'Gender', ct)
        ages = face['AgeRange']
        labels.append("{} < age < {}".format(ages['Low'], ages['High']))
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
    labels = []
    print("checking for celebrity...")
    result = client.recognize_celebrities(
        Image=dict(S3Object={'Bucket': storage.bucket, 'Name': storage.key}))
    celebrities = result['CelebrityFaces']
    if celebrities:
        # only do the first celebrity to keep it simple
        celebrity = celebrities[0]
        labels.append(celebrity['Name'])
        labels.append(celebrity['MatchConfidence'])
        for url in celebrity['Urls']:
            labels.append(url)
    print(labels)
    return labels


def detect_labels(ct) -> []:
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
    lines = []
    print('detecting text...')
    result = client.detect_text(
        Image=dict(S3Object={'Bucket': storage.bucket, 'Name': storage.key}))
    for text in result['TextDetections']:
        if text['Type'] == 'LINE' and text['Confidence'] > ct:
            lines.append(text['DetectedText'])
    if not lines:
        line = ""
        for text in result['TextDetections']:
            if text['Type'] == 'WORD' and text['Confidence'] > ct:
                line += " " + text['DetectedText']
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
