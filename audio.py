import pygame

mute = False


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
