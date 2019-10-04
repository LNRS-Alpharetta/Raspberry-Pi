from PIL import Image, ImageDraw, ImageFont

font_size = 30
font_lib = '/Library/Fonts/Arial.ttf'
font = ImageFont.truetype(font_lib, font_size)
font_color = 'white'
line_color = 'lightgreen'


def load_image(image_file) -> Image:
    return Image.open(image_file)


def annotate_image(image, face, text):
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
        draw.text((left + 4, top + 4), text, font=font, fill=font_color)


def annotate_faces(image, face_result):
    for face in face_result['FaceDetails']:
        annotate_image(image, face, None)


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
