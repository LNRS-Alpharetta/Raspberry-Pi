import picamera
import time


def preview(button):
    time.sleep(0.5)
    with picamera.PiCamera() as camera:
        camera.start_preview()
        while True:
            if button.is_pressed:
                camera.stop_preview()
                break


def capture(image_file):
    with picamera.PiCamera() as camera:
        camera.capture(image_file)
