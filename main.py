import tkinter as tk
import random
import pygame
from space_timer import TimerApp


#used gemini to fix errors and refactor code
#copilot used for most functions
#gemini used for constellation and star functions

# --- INITIAL SETUP ---
pygame.mixer.init()

# Global variables to manage state and canvas objects
planets = []
labels = []
animation_running = False

# --- MUSIC CONTROL FUNCTIONS ---
# Load music with error handling in case the file is missing
try:
    pygame.mixer.music.load("pianoloop.sound.wav")
    pygame.mixer.music.set_volume(0.7)
except pygame.error:
    print("Warning: 'pianoloop.sound.wav' not found. Music functions will be disabled.")
    # Create a dummy music object so the program doesn't crash if the file is missing
    class DummyMusic:
        def play(self, *args): pass
        def pause(self): pass
        def unpause(self): pass
        def stop(self): pass
    pygame.mixer.music = DummyMusic()

def play_music():
    """Plays music from the beginning on a loop."""
    print("Action: Playing music")
    pygame.mixer.music.play(-1)

def pause_music():
    """Pauses the currently playing music."""
    print("Action: Pausing music")
    pygame.mixer.music.pause()

def unpause_music():
    """Resumes the music from where it was paused."""
    print("Action: Unpausing music")
    pygame.mixer.music.unpause()

def stop_music():
    """Stops the music completely."""
    print("Action: Stopping music")
    pygame.mixer.music.stop()

# --- PLANET AND DECORATION DATA ---
planet_facts = [
    "Mercury is the smallest planet",
    "Venus is the hottest planet",
    "A day on Venus is 243 Earth days",
    "Venus is often called the evening star",
    "Saturn is less dense than water",
    "The sunset on Mars is blue",
    "Earth's Moon always shows the same face",
    "It may rain diamonds on Neptune"
]
planet_colors = ["#9B59B6", "#3498DB", "#E74C3C", "#808080", "#00FFFF", "#FFA500", "#FF00FF", "#008080"]

# --- UI AND GRAPHICS SETUP ---
root = tk.Tk()
root.title("Spaced Out")
root.geometry("1000x700")
root.configure(bg="black")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg="black", highlightthickness=0)
canvas.pack(fill="both", expand=True)

# --- GRAPHICS DRAWING FUNCTIONS ---
def add_stars(canvas, num_stars=150):
    star_colors = ["#FFFFFF", "#F0F0F0", "#DDAAEE"]
    for _ in range(num_stars):
        x = random.randint(0, screen_width)
        y = random.randint(0, screen_height)
        size = random.randint(1, 3)
        color = random.choice(star_colors)
        canvas.create_oval(x, y, x + size, y + size, fill=color, outline=color)

def draw_constellations(canvas, num_constellations=6):
    constellation_patterns = [
        [(0, 0), (50, -30), (100, -60), (150, -30), (250, 30), (220, 100), (150, 70)],
        [(0, 250), (100, 100), (150, 0), (100, 100), (200, 50)],
    ]
    for _ in range(num_constellations):
        pattern = random.choice(constellation_patterns)
        start_x = random.randint(50, screen_width - 300)
        start_y = random.randint(50, screen_height - 300)
        for rx, ry in pattern:
            abs_x, abs_y = start_x + rx, start_y + ry
            star_size = 9
            canvas.create_oval(abs_x - star_size/2, abs_y - star_size/2, abs_x + star_size/2, abs_y + star_size/2, fill="#FFFFCC", outline="#FFFFCC")

def planetmaker(canvas):
    """Creates a new set of planets and adds them to the global lists."""
    global planets, labels
    for i in range(len(planet_facts)):
        x = random.randint(80, screen_width - 200)
        y = random.randint(80, screen_height - 200)
        r = 80 + i * 10
        planet = canvas.create_oval(x, y, x + r, y + r, fill=planet_colors[i], outline="")
        center_x, center_y = x + r / 2, y + r / 2
        font_size = max(8, int(r / 10))
        label = canvas.create_text(center_x, center_y, text=planet_facts[i], anchor="center", fill="white", font=("Comic Sans MS", font_size, "bold"), width=r - 10)
        planets.append((planet, r))
        labels.append(label)

# --- CORE ANIMATION AND STATE CONTROL LOGIC ---

def clear_planets():
    """Removes all existing planets and labels from the canvas."""
    global planets, labels
    print("State: Clearing planets")
    for planet, r in planets:
        canvas.delete(planet)
    for label in labels:
        canvas.delete(label)
    planets = []
    labels = []

def animate_planets_right():
    """The main animation loop that moves the planets."""
    if not animation_running:
        return  # Stop the loop if animation is paused
    
    for idx, (planet, r) in enumerate(planets):
        canvas.move(planet, 2, 0)
        canvas.move(labels[idx], 2, 0)
        x1, _, _, _ = canvas.coords(planet)
        if x1 > screen_width: # If planet goes off the right edge, wrap it to the left
            new_y = random.randint(80, screen_height - 200)
            canvas.coords(planet, -r, new_y, 0, new_y + r)
            canvas.coords(labels[idx], -r / 2, new_y + r / 2)
    
    root.after(20, animate_planets_right)

def start_planet_animation():
    """Starts the animation from scratch after clearing any old planets."""
    global animation_running
    if animation_running: return # Prevent starting if already running
    
    print("State: Starting planet animation")
    clear_planets()
    animation_running = True
    planetmaker(canvas)
    animate_planets_right()

def pause_planet_animation():
    """Pauses the animation."""
    global animation_running
    print("State: Pausing planet animation")
    animation_running = False

def resume_planet_animation():
    """Resumes the animation if it was paused."""
    global animation_running
    if not animation_running and planets: # Only resume if paused and planets exist
        print("State: Resuming planet animation")
        animation_running = True
        animate_planets_right()

def reset_all():
    """Stops everything and clears the screen for a full reset."""
    print("State: Resetting application")
    pause_planet_animation()
    clear_planets()
    stop_music()

# --- INITIALIZE AND RUN THE APPLICATION ---
# Draw the static background
add_stars(canvas)
draw_constellations(canvas)

# Create the timer and link its buttons to our control functions
# These keyword arguments now PERFECTLY MATCH the names in the TimerApp class
timer = TimerApp(
    root,
    on_start_animation=start_planet_animation,
    on_play_music=play_music,
    on_pause_animation=pause_planet_animation,
    on_pause_music=pause_music,
    on_resume_animation=resume_planet_animation,
    on_resume_music=unpause_music,
    on_reset=reset_all
)
timer.place(relx=0.5, rely=0.5, anchor="center")

root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))
root.mainloop()
