import rekognition
import storage
import database
import draw
import gpiozero
import picamera
import time

ct = 50
image_file = '/tmp/image.jpg'
button = gpiozero.Button(17)

print("system ready...")
while True:
    # speaker will emit a ready signal when the system is initialized
    # init
    celeb_result = None
    celeb_labels = []
    # object is triggered by a mechanical action - button push
    if button.is_pressed:
        print("working...")
        # speaker emits a countdown
        # capture picture from camera
        camera = picamera.PiCamera()
        camera.capture(image_file)
        # upload picture to S3
        s3 = storage.upload(image_file)
        # call rekognition apis
        # Step 1. Are there faces in the image?
        face_result = rekognition.detect_faces_api(s3)
        face_labels = rekognition.get_face_labels(face_result, ct)
        if face_labels:
            database.inc(face_labels)
        # Step 2. Is the picture of a celebrity?
            celeb_result = rekognition.detect_celebrities_api(s3)
            celeb_labels = rekognition.get_celebrity_labels(celeb_result, ct)
            if celeb_labels:
                database.inc(celeb_labels)
        # Step 3. Are there words?
        text_result = rekognition.detect_text_api(s3)
        text_labels = rekognition.get_text_labels(text_result, ct)
        # Step 4. What else is in the picture?
        label_result = rekognition.detect_labels_api(s3)
        labels = rekognition.get_labels(label_result, ct)
        if labels:
            database.inc(labels)
        # delete local /tmp/image.jpg
        # annotate images
        image = draw.load_image(image_file)
        draw.annotate_celebs(image, celeb_result)
        draw.annotate_faces(image, face_result)
        draw.annotate_labels(image, label_result)
        draw.annotate_text(image, text_result)
        image.show()
        # JavaScript generated on stats
        # website updated with graph and photo booth
        # speaker emits voice of what is analyzed
        print(face_labels)
        print(celeb_labels)
        print(text_labels)
        print(labels)
    time.sleep(0.2)
