import tkinter as tk

class TimerApp(tk.Frame):
    def __init__(self, master, on_start_animation, on_play_music, on_pause_animation, on_pause_music, on_resume_animation, on_resume_music, on_reset):
        # Initialize the frame with a black background and no border
        super().__init__(master, bg="#330524", highlightthickness=0)

        # Store the callback functions from main.py
        self.on_start_animation = on_start_animation
        self.on_play_music = on_play_music
        self.on_pause_animation = on_pause_animation
        self.on_pause_music = on_pause_music
        self.on_resume_animation = on_resume_animation
        self.on_resume_music = on_resume_music
        self.on_reset = on_reset

        # Internal state variables for the timer
        self._timer_job = None
        self.time_left = 0
        self.is_running = False
        self.is_paused = False

        # --- UI Elements for the Timer ---
        self.font_style = ("Comic Sans MS", 16)

        # ### NEW WIDGET: THE TITLE LABEL ###
        self.title_label = tk.Label(
            self,
            text="spaced out",
            font=("Comic Sans MS", 24, "bold"),
            bg="#330524",
            fg="white"
        )
        self.title_label.pack(pady=(0, 20)) # Add padding below the title

        # The entry box for choosing the time
        self.entry = tk.Entry(
            self,
            width=5,
            font=("Comic Sans MS", 40),
            justify='center',
            bg="black",
            fg="white",
            insertbackground="white",
            highlightthickness=0,
            bd=0,
            relief=tk.FLAT
        )
        self.entry.insert(0, "60") # Default to 60 seconds
        self.entry.pack(pady=10)

        # The label for displaying the countdown
        self.label = tk.Label(self, text="00:00", font=("Comic Sans MS", 50, "bold"), bg="#330524", fg="white")
        self.label.pack(pady=10)

        # Frame to hold the control buttons
        button_frame = tk.Frame(self, bg="#330524")
        button_frame.pack(pady=10)
        
        self.start_button = tk.Button(button_frame, text="Start", command=self.handle_start_stop, font=self.font_style, bg="#2ECC71", fg="white", width=8)
        self.start_button.pack(side="left", padx=5)

        self.reset_button = tk.Button(button_frame, text="Reset", command=self.handle_reset, font=self.font_style, bg="#E74C3C", fg="white", width=8)
        self.reset_button.pack(side="left", padx=5)

    def handle_start_stop(self):
        """Handles logic for the Start, Pause, and Resume button."""
        if not self.is_running:
            try:
                if not self.is_paused:
                    # Timer logic is kept in seconds
                    total_seconds = int(self.entry.get())
                    self.time_left = total_seconds
                    self.on_start_animation()
                    self.on_play_music()
                else:
                    self.on_resume_animation()
                    self.on_resume_music()

                self.is_running = True
                self.is_paused = False
                self.start_button.config(text="Pause")
                self.countdown()
            except ValueError:
                self.label.config(text="Invalid Time")
                
        else:
            self.is_running = False
            self.is_paused = True
            self.start_button.config(text="Resume")
            if self._timer_job:
                self.after_cancel(self._timer_job)
            self.on_pause_animation()
            self.on_pause_music()

    def handle_reset(self):
        """Handles the logic for the Reset button."""
        if self._timer_job:
            self.after_cancel(self._timer_job)
        
        self.is_running = False
        self.is_paused = False
        self.time_left = 0
        self.label.config(text="00:00")
        self.start_button.config(text="Start")
        self.on_reset()

    def countdown(self):
        """The main timer loop that updates the label every second."""
        if self.is_running and self.time_left > 0:
            minutes = self.time_left // 60
            seconds = self.time_left % 60
            self.label.config(text=f"{minutes:02d}:{seconds:02d}")
            self.time_left -= 1
            self._timer_job = self.after(1000, self.countdown)
        elif self.time_left <= 0:
            self.label.config(text="Done!")
            self.handle_reset()
