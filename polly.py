import boto3
import audio

polly = boto3.Session().client('polly')
voice = 'Joanna'
file = '/tmp/temp.mp3'


def speak(labels):
    word_string = ""
    for word in labels[0:4]:
        word_string = word_string + ", " + word
    speech = polly.synthesize_speech(Text=word_string,
                                     OutputFormat='mp3',
                                     VoiceId=voice)
    with open(file, 'wb') as writer:
        writer.write(speech['AudioStream'].read())
        writer.close()
    audio.play(file)
