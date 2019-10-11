import pygame

mute = False


def play(audio_file):
    if not mute:
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
