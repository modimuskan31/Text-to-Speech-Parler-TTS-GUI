import tkinter as tk
from tkinter import messagebox

class TTSInputGUI:
    def __init__(self):
        self.root = tk.Tk()
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

        # Submit button frame (always at the bottom)
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=20)
        tk.Button(self.button_frame, text="Generate", command=self.submit).pack()

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
        gender = self.gender_var.get()

        if self.voice_var.get() == "Standard":
            description = f"A standard {gender} expressive and neutral voice with clear pronunciation"
        else:
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
