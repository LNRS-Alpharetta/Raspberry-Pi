import boto3
import storage

client = boto3.client('rekognition')


def detect_faces(ct) -> []:
    # ct  - confidence threshold for API
    # returns a list of faces found, includes all attributes
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
            labels.append('Face')
            check_str(labels, face, 'Gender', ct)
            ages = face['AgeRange']
            labels.append("Age {}-{}".format(ages['Low'], ages['High']))
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
                        labels.append(emotion['Type'].capitalize())
    print(labels)
    return labels


def recognize_celebrities(ct) -> []:
    # ct  - confidence threshold for API
    # returns a list of celebrities found, including any Urls
    # appends the word 'celebrity' as a delimiter
    # example: ['celebrity','John Lennon','www.imdb.com/lennon','celebrity','George Harrison']
    labels = []
    print("checking for celebrity...")
    result = client.recognize_celebrities(
        Image=dict(S3Object={'Bucket': storage.bucket, 'Name': storage.key}))
    celebrities = result['CelebrityFaces']
    if celebrities:
        for celebrity in celebrities:
            if celebrity['MatchConfidence'] > ct:
                labels.append('Celebrity')
                labels.append(celebrity['Name'])
                for url in celebrity['Urls']:
                    labels.append(url)
    print(labels)
    return labels


def detect_labels(ct) -> []:
    # ct  - confidence threshold for API
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
    # ct  - confidence threshold for API
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
        labels.append(attribute['Value'].capitalize())


# Check Boolean Attribute
def check_bool(labels, struct, attr, ct):
    attribute = struct[attr]
    if attribute['Value'] and attribute['Confidence'] > ct:
        labels.append(attr)
