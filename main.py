import rekognition
import storage
import database
import gpiozero
import camera
import draw
import time
import audio
import polly
import os

ct = 50
image_file = '/tmp/image.jpg'
temp_file = '/tmp/test.jpg'
button = gpiozero.Button(17)
ready_message = "[PiCeDoFi-IMAPI-RU] system ready"

try:
    audio.play_mp3("startup_comment.mp3")
    os.system('clear')
    print(ready_message)
    while True:
        celeb_result = None
        celeb_labels = []
        if button.is_pressed:
            print("starting preview...")
            camera.preview(button)
            camera.capture(image_file)
            print('working...')
            audio.play_mp3("intro_comment.mp3")
            # upload picture to S3
            s3 = storage.upload(image_file)
            image = draw.load_image(image_file)
            # call rekognition apis
            # Step 1. Are there faces in the image?
            face_result = rekognition.detect_faces_api(s3)
            face_labels = rekognition.get_face_labels(face_result, ct)
            draw.annotate_faces(image, face_result)
            if face_labels:
                os.system('clear')
                draw.display_text(face_labels)
                database.inc(face_labels)
                audio.play_mp3("faces_comment.mp3")
                polly.speak(face_labels)
            # Step 2. Is the picture of a celebrity?
                celeb_result = rekognition.detect_celebrities_api(s3)
                celeb_labels = rekognition.get_celebrity_labels(celeb_result, ct)
                if celeb_labels:
                    draw.display_text(celeb_labels)
                    database.inc(celeb_labels)
                    for celeb in celeb_labels:
                        audio.play_mp3("celeb_comment.mp3")
                        polly.render_speech(celeb)
                        celeb_image = rekognition.get_celebrity_image(celeb)
                        if celeb_image:
                            draw.preview_image(celeb_image, button)
                        os.system('clear')
                        desc = rekognition.get_celebrity_desc(celeb)
                        print(desc)
                        polly.render_speech(desc)
                        draw.annotate_celebs(image, celeb_result)
                else:
                    audio.play_mp3("no_celeb_comment.mp3")
            # Step 3. If there are no faces, check for words
            else:
                text_result = rekognition.detect_text_api(s3)
                text_labels = rekognition.get_text_labels(text_result, ct)
                if text_labels:
                    draw.display_text(text_labels)
                    audio.play_mp3("text_comment.mp3")
                    polly.speak(text_labels)
                    draw.annotate_text(image, text_result)
                # Step 4. What else is in the picture?
                label_result = rekognition.detect_labels_api(s3)
                labels = rekognition.get_labels(label_result, ct)
                if labels:
                    os.system('clear')
                    draw.display_text(labels)
                    database.inc(labels)
                    audio.play_mp3("labels_comment.mp3")
                    polly.speak(labels)
                    draw.annotate_labels(image, label_result)
            draw.save_image(image, temp_file)
            # Upload annotated image to S3
            storage.upload(temp_file)
            audio.play_mp3("closure_comment.mp3")
            storage.delete(s3['S3Object']['Name'])
            draw.preview_image(temp_file, button)
            os.system('clear')
            print(ready_message)
        time.sleep(0.1)
except KeyboardInterrupt:
    print("...request to stop program...")
finally:
    audio.play_mp3("exception_comment.mp3")
    print("[PiCeDoFi-IMAPI-RU] process ended")
