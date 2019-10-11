import boto3
import audio

polly = boto3.Session().client('polly')
voice = 'Joanna'
file = '/tmp/temp.mp3'


def speak(word):
    single_list = [word]
    speak(single_list)


def speak(labels, limit=True):
    word_string = ""
    list_length = 5
    if not limit:
        list_length = len(labels)
    for word in labels[0:list_length]:
        word_string = word_string + ", " + word
    speech = polly.synthesize_speech(Text=word_string,
                                     OutputFormat='mp3',
                                     VoiceId=voice)
    with open(file, 'wb') as writer:
        writer.write(speech['AudioStream'].read())
        writer.close()
    audio.play(file)
