import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pyttsx3
from gtts import gTTS
import threading

class TextToSpeechApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text-to-Speech Application")
        self.root.geometry("800x600")  # Set initial size
        self.root.minsize(600, 400)    # Set minimum size
        self.center_window()          # Center window on screen
        self.root.attributes('-topmost', True)  # Bring window to front
        self.root.attributes('-topmost', False)  # Allow window to lose focus

        self.create_widgets()
        self.setup_tts()

    def center_window(self):
        # Get screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate position x and y coordinates to center window
        x = (screen_width // 2) - (800 // 2)
        y = (screen_height // 2) - (600 // 2)

        self.root.geometry(f'800x600+{x}+{y}')

    def create_widgets(self):
        style = ttk.Style()
        style.configure("TLabel", font=("Helvetica", 12))
        style.configure("TButton", font=("Helvetica", 12), padding=6)
        style.configure("TCombobox", font=("Helvetica", 12), padding=6)
        style.configure("TScale", font=("Helvetica", 12), padding=6)

        self.main_frame = ttk.Frame(self.root, padding="10 10 10 10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.text_label = ttk.Label(self.main_frame, text="Enter Text:")
        self.text_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        self.text_entry = tk.Text(self.main_frame, height=10, width=70, font=("Helvetica", 12))
        self.text_entry.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

        self.language_label = ttk.Label(self.main_frame, text="Select Language:")
        self.language_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

        self.language_var = tk.StringVar()
        self.language_options = ttk.Combobox(self.main_frame, textvariable=self.language_var, state='readonly')
        self.language_options['values'] = ('en', 'es', 'fr', 'de', 'zh')
        self.language_options.set('en')
        self.language_options.grid(row=2, column=1, padx=5, pady=5)

        self.voice_label = ttk.Label(self.main_frame, text="Select Voice:")
        self.voice_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)

        self.voice_var = tk.StringVar()
        self.voice_options = ttk.Combobox(self.main_frame, textvariable=self.voice_var, state='readonly')
        self.voice_options['values'] = ('Male', 'Female')
        self.voice_options.set('Male')
        self.voice_options.grid(row=3, column=1, padx=5, pady=5)

        self.rate_label = ttk.Label(self.main_frame, text="Speech Rate:")
        self.rate_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)

        self.rate_slider = ttk.Scale(self.main_frame, from_=100, to=300, orient=tk.HORIZONTAL)
        self.rate_slider.set(200)
        self.rate_slider.grid(row=4, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))

        self.volume_label = ttk.Label(self.main_frame, text="Volume:")
        self.volume_label.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)

        self.volume_slider = ttk.Scale(self.main_frame, from_=50, to=100, orient=tk.HORIZONTAL)
        self.volume_slider.set(100)
        self.volume_slider.grid(row=5, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))

        self.button_frame = ttk.Frame(self.main_frame, padding="5 5 5 5")
        self.button_frame.grid(row=6, column=0, columnspan=2, pady=10)

        self.play_button = ttk.Button(self.button_frame, text="Play", command=self.play_text, style="TButton")
        self.play_button.grid(row=0, column=0, padx=5, pady=5)

        self.pause_button = ttk.Button(self.button_frame, text="Pause", command=self.pause_text, state=tk.DISABLED, style="TButton")
        self.pause_button.grid(row=0, column=1, padx=5, pady=5)

        self.resume_button = ttk.Button(self.button_frame, text="Resume", command=self.resume_text, state=tk.DISABLED, style="TButton")
        self.resume_button.grid(row=0, column=2, padx=5, pady=5)

        self.stop_button = ttk.Button(self.button_frame, text="Stop", command=self.stop_text, state=tk.DISABLED, style="TButton")
        self.stop_button.grid(row=0, column=3, padx=5, pady=5)

        self.save_button = ttk.Button(self.button_frame, text="Save as MP3", command=self.save_as_mp3, style="TButton")
        self.save_button.grid(row=0, column=4, padx=5, pady=5)

        self.clear_button = ttk.Button(self.button_frame, text="Clear", command=self.clear_text, style="TButton")
        self.clear_button.grid(row=0, column=5, padx=5, pady=5)

        self.import_button = ttk.Button(self.button_frame, text="Import Text", command=self.import_text, style="TButton")
        self.import_button.grid(row=0, column=6, padx=5, pady=5)

        self.status_label = ttk.Label(self.main_frame, text="", foreground="blue")
        self.status_label.grid(row=7, column=0, columnspan=2, pady=5)

    def setup_tts(self):
        self.engine = pyttsx3.init()
        self.is_playing = False
        self.current_text = ""
        self.play_thread = None  # Thread to handle speech synthesis

    def play_text(self):
        text = self.text_entry.get("1.0", tk.END).strip()
        if not text:
            messagebox.showerror("Error", "Text input is empty.")
            return

        self.current_text = text
        voice = self.voice_var.get()
        rate = self.rate_slider.get()
        volume = self.volume_slider.get() / 100  # Convert volume to a float between 0 and 1

        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)

        voices = self.engine.getProperty('voices')
        if voice == 'Female':
            self.engine.setProperty('voice', voices[1].id)
        else:
            self.engine.setProperty('voice', voices[0].id)

        # Check if a speech synthesis thread is already running
        if self.play_thread and self.play_thread.is_alive():
            messagebox.showwarning("Warning", "Speech is already playing.")
            return

        # Update button states
        self.play_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL)
        self.resume_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        # Start speech synthesis in a separate thread
        self.play_thread = threading.Thread(target=self._play_in_thread, args=(text,))
        self.play_thread.start()

    def _play_in_thread(self, text):
        self.is_playing = True
        self.engine.say(text)
        self.engine.runAndWait()
        self.is_playing = False

        # Reset button states after speech is finished
        self.play_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.resume_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.DISABLED)

    def pause_text(self):
        if self.is_playing:
            self.engine.stop()  # Stop speech completely
            self.is_playing = False
            self.status_label.config(text="Paused")

            # Update button states
            self.play_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.DISABLED)
            self.resume_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

    def resume_text(self):
        if not self.is_playing:
            # Restart speech from the beginning of the paused segment
            self.play_text()

    def stop_text(self):
        if self.is_playing:
            self.engine.stop()
            self.is_playing = False
            self.status_label.config(text="Stopped")

            # Reset button states
            self.play_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.DISABLED)
            self.resume_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.DISABLED)

    def save_as_mp3(self):
        text = self.text_entry.get("1.0", tk.END).strip()
        if not text:
            messagebox.showerror("Error", "Text input is empty.")
            return

        lang = self.language_var.get()
        tts = gTTS(text=text, lang=lang)
        save_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3"), ("All files", "*.*")])
        if save_path:
            tts.save(save_path)
            messagebox.showinfo("Success", f"Audio saved as {save_path}")

    def clear_text(self):
        self.text_entry.delete("1.0", tk.END)
        self.status_label.config(text="Text cleared")

    def import_text(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.text_entry.delete("1.0", tk.END)
                self.text_entry.insert(tk.END, content)
                self.status_label.config(text="Text imported")

if __name__ == "__main__":
    root = tk.Tk()
    app = TextToSpeechApp(root)
    root.mainloop()
