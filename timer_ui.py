import tkinter as tk
from tkinter import messagebox

# timer_ui.py
# Simple Tkinter timer where the user sets the time (seconds or MM:SS) and can Start/Pause/Reset.


class TimerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple Timer")
        self.resizable(False, False)

        self.original_secs = 0
        self.remaining = 0
        self._job = None
        self.paused = True

        tk.Label(self, text="Set time (seconds or MM:SS):").grid(row=0, column=0, padx=8, pady=8)
        self.entry = tk.Entry(self, width=12)
        self.entry.grid(row=0, column=1, padx=8, pady=8)
        self.entry.insert(0, "60")  # default 60 seconds

        self.time_label = tk.Label(self, text=self._format_time(0), font=("Comic Sans MS", 24))
        self.time_label.grid(row=1, column=0, columnspan=2, padx=8, pady=(0, 12))

        btn_frame = tk.Frame(self)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=(0,8))

        self.start_btn = tk.Button(btn_frame, text="Start", width=8, command=self.start)
        self.start_btn.pack(side="left", padx=4)
        self.pause_btn = tk.Button(btn_frame, text="Pause", width=8, state="disabled", command=self.toggle_pause)
        self.pause_btn.pack(side="left", padx=4)
        self.reset_btn = tk.Button(btn_frame, text="Reset", width=8, state="disabled", command=self.reset)
        self.reset_btn.pack(side="left", padx=4)

    def _format_time(self, secs):
        mins = secs // 60
        s = secs % 60
        return f"{mins:02d}:{s:02d}"

    def _parse_input(self, text):
        text = text.strip()
        if ":" in text:
            parts = text.split(":")
            if len(parts) != 2:
                raise ValueError("Invalid MM:SS format")
            mins = int(parts[0])
            secs = int(parts[1])
            return mins * 60 + secs
        return int(text)

    def start(self):
        try:
            secs = self._parse_input(self.entry.get())
        except Exception:
            messagebox.showerror("Invalid input", "Enter seconds (e.g. 90) or MM:SS (e.g. 1:30).")
            return

        if secs <= 0:
            messagebox.showerror("Invalid input", "Please enter a positive time.")
            return

        self.original_secs = secs
        self.remaining = secs
        self.entry.config(state="disabled")
        self.start_btn.config(state="disabled")
        self.pause_btn.config(state="normal", text="Pause")
        self.reset_btn.config(state="normal")
        self.paused = False
        self._tick()  # start countdown immediately

    def toggle_pause(self):
        if self.paused:
            # resume
            self.paused = False
            self.pause_btn.config(text="Pause")
            self._tick()
        else:
            # pause
            self.paused = True
            self.pause_btn.config(text="Resume")
            if self._job:
                self.after_cancel(self._job)
                self._job = None

    def reset(self):
        self.paused = True
        if self._job:
            self.after_cancel(self._job)
            self._job = None
        self.remaining = self.original_secs
        self.time_label.config(text=self._format_time(self.remaining))
        self.entry.config(state="normal")
        self.start_btn.config(state="normal")
        self.pause_btn.config(state="disabled", text="Pause")
        self.reset_btn.config(state="disabled")

    def _tick(self):
        if self.paused:
            return
        self.time_label.config(text=self._format_time(self.remaining))
        if self.remaining <= 0:
            self._on_finish()
            return
        self.remaining -= 1
        self._job = self.after(1000, self._tick)

    def _on_finish(self):
        self.time_label.config(text="00:00")
        self.entry.config(state="normal")
        self.start_btn.config(state="normal")
        self.pause_btn.config(state="disabled", text="Pause")
        self.reset_btn.config(state="disabled")
        self.paused = True
        messagebox.showinfo("Timer", "Time's up!")

if __name__ == "__main__":
    app = TimerApp()
    app.mainloop()