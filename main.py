import rekognition
import storage
import database
import draw
import gpiozero
import picamera
import time
import audio
import polly

ct = 50
image_file = '/tmp/image.jpg'
temp_file = '/tmp/test.jpg'
button = gpiozero.Button(17)

# speaker will emit a ready signal when the system is initialized
audio.play('./mp3/startup_comment.mp3')
print("system ready...")
while True:
    # init
    celeb_result = None
    celeb_labels = []
    # object is triggered by a button push
    if button.is_pressed:
        audio.play('./mp3/intro_comment.mp3')
        print("working...")
        # capture picture from camera
        with picamera.PiCamera() as camera:
            camera.capture(image_file)
        # upload picture to S3
        s3 = storage.upload(image_file)
        # call rekognition apis
        # Step 1. Are there faces in the image?
        face_result = rekognition.detect_faces_api(s3)
        face_labels = rekognition.get_face_labels(face_result, ct)
        if face_labels:
            database.inc(face_labels)
            audio.play('./mp3/faces_comment.mp3')
            print(face_labels)
            polly.speak(face_labels)
        # Step 2. Is the picture of a celebrity?
            celeb_result = rekognition.detect_celebrities_api(s3)
            celeb_labels = rekognition.get_celebrity_labels(celeb_result, ct)
            if celeb_labels:
                database.inc(celeb_labels)
                audio.play('./mp3/celeb_comment.mp3')
                print(celeb_labels)
                polly.speak(celeb_labels)
            else:
                audio.play('./mp3/no_celeb_comment.mp3')
        # Step 3. Are there words?
        text_result = rekognition.detect_text_api(s3)
        text_labels = rekognition.get_text_labels(text_result, ct)
        if text_labels: 
            audio.play('./mp3/text_comment.mp3')
            print(text_labels)
            polly.speak(text_labels)
        # Step 4. What else is in the picture?
        label_result = rekognition.detect_labels_api(s3)
        labels = rekognition.get_labels(label_result, ct)
        if labels:
            database.inc(labels)
            audio.play('./mp3/labels_comment.mp3')
            print(labels)
            polly.speak(labels)
        # annotate image
        image = draw.load_image(image_file)
        draw.annotate_celebs(image, celeb_result)
        draw.annotate_faces(image, face_result)
        draw.annotate_labels(image, label_result)
        draw.annotate_text(image, text_result)
        draw.save_image(image, temp_file)
        # Upload annotated image to S3
        storage.upload(temp_file)
        # website updated with graph and photo booth
        audio.play('./mp3/closure_comment.mp3')
        print("system ready...")
    time.sleep(0.2)
