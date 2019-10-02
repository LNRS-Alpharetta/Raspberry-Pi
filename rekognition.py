import boto3

client = boto3.client('rekognition')


def detect_faces_api(bucket) -> str:
    return client.detect_faces(Image=bucket, Attributes=['ALL'])


def detect_celebrities_api(bucket) -> str:
    return client.recognize_celebrities(Image=bucket)


def detect_labels_api(bucket) -> str:
    return client.detect_labels(Image=bucket)


def detect_text_api(bucket) -> str:
    return client.detect_text(Image=bucket)


def get_face_labels(result, ct) -> []:
    # result  - result from the API call
    # ct - confidence threshold to limit return values
    # returns a list of faces found, includes all attributes
    # appends the word 'face' as a delimiter
    # example: ['face','male','age 23-35','face','female','age 35-45]']
    labels = []
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
    return labels


def get_celebrity_labels(result, ct) -> []:
    # result  - result from the API call
    # ct  - confidence threshold to limit return values
    # returns a list of celebrities found
    # appends the word 'celebrity' as a delimiter
    # example: ['celebrity','John Lennon','celebrity','George Harrison']
    labels = []
    celebrities = result['CelebrityFaces']
    if celebrities:
        for celebrity in celebrities:
            if celebrity['MatchConfidence'] > ct:
                labels.append('Celebrity')
                labels.append(celebrity['Name'])

    return labels


def get_celebrity_urls(result, name) -> []:
    # result  - result from the API call
    # name - celebrity name
    # Returns a list of URLs for a given celebrity
    urls = []
    celebrities = result['CelebrityFaces']
    if celebrities:
        for celebrity in celebrities:
            if celebrity['Name'] == name:
                urls = urls + celebrity['Urls']
    return urls


def get_text_labels(result, ct) -> []:
    # result  - result from the API call
    # ct  - confidence threshold to limit return values
    # detects text and returns lines and words
    labels = []
    for text in result['TextDetections']:
        if (text['Type'] == 'LINE' or text['Type'] == 'WORD') and text['Confidence'] > ct:
            labels.append(text['DetectedText'])
    return labels


def get_labels(result, ct) -> []:
    # result  - result from the API call
    # ct  - confidence threshold to limit return values
    # returns a list of labels found - excluding the word Face
    # example: ['Person','Human','Shoe']
    labels = []
    for label in result['Labels']:
        if label['Confidence'] >= ct:
            labels.append(label['Name'])
    return labels.remove("Face")


def check_str(labels, struct, attr, ct):
    # Check String Attribute
    attribute = struct[attr]
    if attribute['Confidence'] > ct:
        labels.append(attribute['Value'].capitalize())


def check_bool(labels, struct, attr, ct):
    # Check Boolean Attribute
    attribute = struct[attr]
    if attribute['Value'] and attribute['Confidence'] > ct:
        labels.append(attr)
