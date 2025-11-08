import pygame

# Initialize pygame mixer
pygame.mixer.init()
pygame.mixer.music.load("Tape.wav")
pygame.mixer.music.set_volume(0.7)

def play():
    pygame.mixer.music.play(-1)  # -1 means loop indefinitely

def stop():
    pygame.mixer.music.stop()

def pause():
    pygame.mixer.music.pause()

def unpause():
    pygame.mixer.music.unpause()
