import tkinter as tk
from tkinter import messagebox

class TTSInputGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Welcome to Parler Text to Speech!")
        self.root.geometry("500x500")

        # Prompt
        tk.Label(self.root, text="Enter Prompt to Speak:").pack()
        self.prompt_entry = tk.Text(self.root, height=4, width=50)
        self.prompt_entry.pack()

        # Voice selection
        self.voice_var = tk.StringVar(value="random")
        tk.Label(self.root, text="Voice Selection:").pack()
        tk.Radiobutton(self.root, text="Standard", variable=self.voice_var, value="Standard", command=self.toggle_custom).pack()
        tk.Radiobutton(self.root, text="Custom", variable=self.voice_var, value="custom", command=self.toggle_custom).pack()

        # Custom voice options (initially hidden)
        self.custom_frame = tk.Frame(self.root)
        tk.Label(self.custom_frame, text="Gender:").pack()
        self.gender_var = tk.StringVar(value="female")
        tk.OptionMenu(self.custom_frame, self.gender_var, "male", "female").pack()

        tk.Label(self.custom_frame, text="Background:").pack()
        self.background_var = tk.StringVar(value="clear")
        tk.OptionMenu(self.custom_frame, self.background_var, "noisy", "clear", "slightly noisy").pack()

        tk.Label(self.custom_frame, text="Speech Type:").pack()
        self.speech_type_var = tk.StringVar(value="monotone")
        tk.OptionMenu(self.custom_frame, self.speech_type_var, "monotone", "excited", "expressive").pack()

        self.custom_frame.pack_forget()

        # Submit button
        tk.Button(self.root, text="Generate", command=self.submit).pack(pady=20)

        self.user_input = None

    def toggle_custom(self):
        if self.voice_var.get() == "custom":
            self.custom_frame.pack()
        else:
            self.custom_frame.pack_forget()

    def submit(self):
        prompt = self.prompt_entry.get("1.0", tk.END).strip()
        if not prompt:
            messagebox.showerror("Error", "Prompt cannot be empty!")
            return

        if self.voice_var.get() == "random":
            description = "A random expressive voice"
        else:
            gender = self.gender_var.get()
            background = self.background_var.get()
            speech_type = self.speech_type_var.get()
            description = f"The {gender} speaker's voice is {speech_type} tone with a {background} background"

        self.user_input = {
            "prompt": prompt,
            "description": description
        }
        self.root.quit()  # Close the GUI

    def run(self):
        self.root.mainloop()
        return self.user_input
