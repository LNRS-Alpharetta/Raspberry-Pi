import boto3
import audio

polly = boto3.Session().client('polly')
voice = 'Joanna'
file = '/tmp/temp.mp3'


def speak_word(word):
    render_speech(word)


def speak(labels, limit=True):
    word_string = ""
    list_length = 5
    if not limit:
        list_length = len(labels)
    for word in labels[0:list_length]:
        word_string = word_string + ", " + word
    render_speech(word_string)


def render_speech(text):
    speech_text = "<speak>" + text + "</speak>"
    speech = polly.synthesize_speech(Text=speech_text,
                                     OutputFormat='mp3',
                                     TextType='ssml',
                                     VoiceId=voice)
    with open(file, 'wb') as writer:
        writer.write(speech['AudioStream'].read())
        writer.close()
    audio.play(file)
