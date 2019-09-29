import rekognition
import database
import storage

ct = 90

while True:
    # init
    celebrity = []
    # speaker will emit a ready signal when the system is initialized
    # object is triggered by a mechanical action - button push
    # speaker emits a countdown
    # capture picture from camera
    # save picture to /tmp/image.jpg
    # upload picture to S3
    storage.upload("./img/image.png")
    # delete /tmp/image.jpg
    # call rekognition apis
    # Step 1. Are there faces in the image?
    face = rekognition.detect_faces(ct)
    if face:
        database.increment_label_counts(face)
        # Step 2. Is the picture of a celebrity?
        celebrity = rekognition.recognize_celebrities()
        if celebrity:
            database.increment_label_count(celebrity[0])
    # Step 3. What else is in the picture?
    labels = rekognition.detect_labels(ct)
    if labels:
        database.increment_label_counts(labels)
    # Step 4. Are there words?
    lines = rekognition.detect_text(ct)
    # archive working file in bucket root
    # storage.archive()
    # JavaScript generated on stats
    # website updated with graph and photo booth
    # speaker emits voice of what is analyzed
    break
