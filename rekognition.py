import boto3
import database
import imdb
import re

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
    # example: ['male','age 23-35','female','age 35-45]']
    labels = []
    faces = result['FaceDetails']
    if faces:
        for face in faces:
            check_str(labels, face, 'Gender', ct)
            emotions = face['Emotions']
            if emotions:
                for emotion in emotions:
                    if emotion['Confidence'] > ct:
                        labels.append(emotion['Type'].capitalize())
            ages = face['AgeRange']
            labels.append("Age {}-{}".format(ages['Low'], ages['High']))
            check_bool(labels, face, 'Smile', ct)
            check_bool(labels, face, 'Eyeglasses', ct)
            check_bool(labels, face, 'Sunglasses', ct)
            check_bool(labels, face, 'Beard', ct)
            check_bool(labels, face, 'Mustache', ct)
            check_bool(labels, face, 'EyesOpen', ct)
            check_bool(labels, face, 'MouthOpen', ct)
    return labels


def get_celebrity_labels(result, ct) -> []:
    # result  - result from the API call
    # ct  - confidence threshold to limit return values
    # returns a list of celebrities found
    # example: ['John Lennon','Paul McCartney','George Harrison']
    labels = []
    celebrities = result['CelebrityFaces']
    if celebrities:
        for celebrity in celebrities:
            confidence = celebrity['MatchConfidence']
            database.insert_trend(confidence)
            labels.append(celebrity['Name'])
    return labels


def get_celebrity_desc(celeb_name) -> str:
    ia = imdb.IMDb()
    celeb_search = ia.search_person(celeb_name)
    find = re.findall(r'\d+', str(celeb_search))
    celeb_id = list(map(int, find))[0]
    person = ia.get_person(celeb_id)
    biog = person['biography'][0]
    dot_end = biog.find('.', 100, 500)
    wc = len(biog.split())
    text = biog[0:dot_end]
    parsed_text = text.replace('.', '. ')
    print(parsed_text)
    return parsed_text


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
        confidence = text['Confidence']
        database.insert_trend(confidence)
        if (text['Type'] == 'LINE' or text['Type'] == 'WORD') and confidence > ct:
            labels.append(text['DetectedText'])
    return labels


def get_labels(result, ct) -> []:
    # result  - result from the API call
    # ct  - confidence threshold to limit return values
    # returns a list of labels found
    # labels with instances will be first
    # example: ['Shoe','Person','Human']
    instances = []
    labels = []
    for label in result['Labels']:
        confidence = label['Confidence']
        database.insert_trend(confidence)
        if confidence >= ct:
            name = label["Name"]
            if len(label['Instances']) > 0:
                instances.append(name)
            else:
                labels.append(name)
    return instances.append(labels)


def check_str(labels, struct, attr, ct):
    # Check String Attribute
    attribute = struct[attr]
    confidence = attribute['Confidence']
    database.insert_trend(confidence)
    if confidence > ct:
        labels.append(attribute['Value'].capitalize())


def check_bool(labels, struct, attr, ct):
    # Check Boolean Attribute
    attribute = struct[attr]
    confidence = attribute['Confidence']
    database.insert_trend(confidence)
    if attribute['Value'] and confidence > ct:
        labels.append(attr)
