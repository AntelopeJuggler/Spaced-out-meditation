import pygame
import threading
import time

def check_for_stop():
    global should_stop
    input("Press Enter to stop playback...")
    should_stop = True

# Initialize pygame mixer
pygame.mixer.init()
pygame.mixer.music.load("Tape.wav")  # Using the WAV file instead of opus
pygame.mixer.music.set_volume(0.7)  # Set volume (0.0 to 1.0)

# Start playing
print("Starting playback...")
pygame.mixer.music.play()

# Create and start input thread
should_stop = False
input_thread = threading.Thread(target=check_for_stop)
input_thread.start()

# Main loop
while pygame.mixer.music.get_busy() and not should_stop:
    time.sleep(0.1)

pygame.mixer.music.stop()
print("Playback stopped.")
