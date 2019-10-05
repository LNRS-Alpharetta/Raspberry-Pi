from PIL import Image, ImageDraw, ImageFont
import platform


font_lib = None
font_size = 30
if platform.system() == 'Darwin':
    font_lib = '/Library/Fonts/Arial.ttf'
else:
    font_lib = '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.tff'
label_font = ImageFont.truetype(font_lib, font_size)


def load_image(image_file) -> Image:
    return Image.open(image_file)


def annotate_image(image, face, text, text_left=4, text_top=4, font=label_font,
                   font_color='white', line_color='lightgreen'):
    img_width, img_height = image.size
    draw = ImageDraw.Draw(image)
    box = face['BoundingBox']
    left = img_width * box['Left']
    top = img_height * box['Top']
    width = img_width * box['Width']
    height = img_height * box['Height']
    points = (
        (left, top), (left + width, top), (left + width, top + height),
        (left, top + height), (left, top))
    draw.line(points, fill=line_color, width=2)
    if text:
        draw.text((left + text_left, top + text_top), text, font=font, fill=font_color)


def annotate_faces(image, face_result):
    for face in face_result['FaceDetails']:
        emotions = face['Emotions']
        if emotions:
            for emotion in emotions:
                if emotion['Confidence'] > 90:
                    annotate_image(image, face, emotion['Type'],
                                   font_color='white', text_top=-30)


def annotate_celebs(image, celeb_result):
    celebrities = celeb_result['CelebrityFaces']
    if celebrities:
        for celebrity in celebrities:
            annotate_image(image, celebrity['Face'], celebrity['Name'])


def annotate_labels(image, label_result):
    labels = label_result['Labels']
    if labels:
        for label in labels:
            instances = label['Instances']
            if instances:
                for instance in instances:
                    annotate_image(image, instance, label['Name'])


def annotate_text(image, text_result):
    labels = text_result['TextDetections']
    if labels:
        for label in labels:
            text = label['Geometry']
            annotate_image(image, text, None, line_color='black')
