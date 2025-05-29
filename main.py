from gui import TTSInputGUI
import tts_logic


def main():
    gui = TTSInputGUI()
    user_input = gui.run()

    if user_input:
        prompt = user_input["prompt"]
        description = user_input["description"]
        print("Generating speech with the following settings:")
        print(f"Prompt: {prompt}")
        print(f"Voice Description: {description}")

        tts_logic.generate_audio(prompt, description)

if __name__ == "__main__":
    main()