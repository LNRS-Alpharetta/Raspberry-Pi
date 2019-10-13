import boto3
import audio

polly = boto3.Session().client('polly')


def speak_words(word, paragraph=False):
    if paragraph:
        word = "<p>" + word + "/<p>"
    render_speech(word)


def speak(labels, limit=True):
    word_string = ""
    list_length = 5
    if not limit:
        list_length = len(labels)
    for word in labels[0:list_length]:
        word_string = word_string + ", " + word
    render_speech(word_string)


def render_speech(text, file='/tmp/temp.mp3', voice='Joanna', engine='standard'):
    speech_text = "<speak>" + text + "</speak>"
    speech = polly.synthesize_speech(Text=speech_text,
                                     OutputFormat='mp3',
                                     TextType='ssml',
                                     VoiceId=voice,
                                     Engine=engine)
    with open(file, 'wb') as writer:
        writer.write(speech['AudioStream'].read())
        writer.close()
    audio.play(file)
