import threading
import logging
import time

import tkinter as tk
from tkinter import ttk, messagebox
import torch

from tts_logic import TTSLogic

class TTSInputGUI:
    def __init__(self):
        self.user_input = None
        self.tts_logic = TTSLogic()


        self.root = tk.Tk()
        self.root.title("Welcome to Parler Text to Speech!")

        # Progress bar frame at the top
        self.progress_frame = tk.Frame(self.root)
        self.progress_frame.pack(pady=10)

        self.progress_label = tk.Label(self.progress_frame, text="", font=("Arial", 10))
        self.progress_label.pack()

        self.progress_bar = ttk.Progressbar(self.progress_frame, orient="horizontal", length=300, mode="determinate",
                                            maximum= 100)
        self.progress_bar.pack()
        self.progress_frame.pack_forget()  # Initially hidden

        # Create main frame to hold everything
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=10)

        # Prompt
        tk.Label(self.main_frame, text="Enter Prompt to Speak:").pack()
        self.prompt_entry = tk.Text(self.main_frame, height=4, width=50)
        self.prompt_entry.pack()

        # Voice selection
        tk.Label(self.main_frame, text="Voice Selection:").pack()
        self.voice_var = tk.StringVar(value="standard")
        tk.Radiobutton(self.main_frame, text="Standard", variable=self.voice_var, value="standard",
                       command=self.toggle_custom).pack()
        tk.Radiobutton(self.main_frame, text="Custom", variable=self.voice_var, value="custom",
                       command=self.toggle_custom).pack()

        # Gender (always visible)
        tk.Label(self.main_frame, text="Gender:").pack()
        self.gender_var = tk.StringVar(value="female")
        tk.OptionMenu(self.main_frame, self.gender_var, "male", "female").pack()

        # Custom voice options (toggle visibility)
        self.custom_frame = tk.Frame(self.main_frame)
        tk.Label(self.custom_frame, text="Background:").pack()
        self.background_var = tk.StringVar(value="clear")
        tk.OptionMenu(self.custom_frame, self.background_var, "noisy", "clear", "slightly noisy").pack()

        tk.Label(self.custom_frame, text="Speech Type:").pack()
        self.speech_type_var = tk.StringVar(value="monotone")
        tk.OptionMenu(self.custom_frame, self.speech_type_var, "monotone", "excited", "expressive").pack()

        # Submit & Close buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=20)

        tk.Button(self.button_frame, text="Generate", command=self.submit).pack(side="left", padx=10)
        tk.Button(self.button_frame, text="Close App", command=self.root.quit).pack(side="left", padx=10)

        self.play_button = tk.Button(self.button_frame, text="Play Audio", state="disabled", command=self.play_audio)
        self.play_button.pack(pady=5)

        self.audio_path = None

    def toggle_custom(self):
        if self.voice_var.get() == "custom":
            self.custom_frame.pack()
        else:
            self.custom_frame.pack_forget()

    def generate_and_close(self):

        try:
            self.progress_bar["value"] = 20
            self.progress_label.config(text="Loading model...")
            self.root.update_idletasks()

            device = "cpu"

            # Load model and tokenizer
            model = self.tts_logic.load_model(device)
            tokenizer = self.tts_logic.load_tokenizer()

            self.progress_bar["value"] = 40
            self.progress_label.config(text="Tokenizing inputs...")
            self.root.update_idletasks()
            time.sleep(0.3)

            # Tokenize input
            input_ids, prompt_input_ids = self.tts_logic.prepare_inputs(tokenizer, self.user_input["prompt"],
                                                                   self.user_input["description"], device)

            self.progress_bar["value"] = 60
            self.progress_label.config(text="Generating audio...")
            self.root.update_idletasks()
            time.sleep(0.3)

            # Generate speech
            audio_arr, sampling_rate = self.tts_logic.run_generation(model, input_ids, prompt_input_ids)

            self.progress_bar["value"] = 80
            self.progress_label.config(text="Saving audio...")
            self.root.update_idletasks()
            time.sleep(0.3)

            output_path = self.tts_logic.save_audio(audio_arr, sampling_rate)

            self.progress_bar["value"] = 100
            self.progress_label.config(text="Completed!")
            self.root.update_idletasks()
            time.sleep(0.5)

            self.progress_label.config(text="Playing the audio...")
            self.root.update_idletasks()

            # Schedule the audio playback safely on the main GUI thread
            self.audio_path = output_path
            self.progress_label.config(text="Audio ready. Click 'Play' to listen.")
            self.play_button.config(state="normal")  # Enable the play button



        except Exception as e:
            logging.exception(f"Error occurred: {e}")
            self.progress_label.config(text="Error occurred!")
        finally:
            self.progress_bar.stop()

    def play_audio(self):
        if self.audio_path:
            try:
                self.tts_logic.play_audio(self.audio_path)
            except Exception as e:
                logging.exception(f"Playback error: {e}")
                messagebox.showerror("Playback Error", "Could not play audio.")

    def submit(self):
        prompt = self.prompt_entry.get("1.0", tk.END).strip()
        if not prompt:
            messagebox.showerror("Error", "Prompt cannot be empty!")
            return

        gender = self.gender_var.get()

        if self.voice_var.get().lower() == "standard":
            description = f"A standard {gender} expressive and neutral voice with clear pronunciation"
        else:
            background = self.background_var.get()
            speech_type = self.speech_type_var.get()
            description = f"The {gender} speaker's voice is {speech_type} tone with a {background} background"

        self.user_input = {
            "prompt": prompt,
            "description": description
        }

        # Show progress bar
        self.progress_label.config(text="Generating...")
        self.progress_frame.pack()
        self.progress_bar.start()

        # Start a thread to generate the audio
        thread = threading.Thread(target=self.generate_and_close)
        thread.start()

    def run(self):
        self.root.mainloop()
        return self.user_input
