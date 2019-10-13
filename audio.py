import pygame

mute = False
mp3_dir = '/home/pi/mp3'


def muted():
    return mute


def play(audio_file):
    if not muted():
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue


def play_mp3(mp3_file):
    play("{}/{}".format(mp3_dir,mp3_file))
