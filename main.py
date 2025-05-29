import logging

from gui import TTSInputGUI

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    logging.basicConfig(
        filename="tts_app.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    gui = TTSInputGUI()
    user_input = gui.run()

    if user_input:
        logging.info("User input received:")
        logging.info(f"Prompt: {user_input['prompt']}")
        logging.info(f"Voice Description: {user_input['description']}")

if __name__ == "__main__":
    main()