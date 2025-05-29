import soundfile as sf
import simpleaudio as sa

from transformers import AutoTokenizer
from parler_tts import ParlerTTSForConditionalGeneration


class TTSLogic:

    def load_model(self, device="cpu"):
        return ParlerTTSForConditionalGeneration.from_pretrained(
            "parler-tts/parler-tts-mini-v1"
        ).to(device)

    def load_tokenizer(self):
        return AutoTokenizer.from_pretrained("parler-tts/parler-tts-mini-v1")

    def prepare_inputs(self, tokenizer, prompt, description, device):
        input_ids = tokenizer(description, return_tensors="pt").input_ids.to(device)
        prompt_input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)
        return input_ids, prompt_input_ids

    def run_generation(self, model, input_ids, prompt_input_ids):
        generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)
        audio_arr = generation.cpu().numpy().squeeze()
        return audio_arr, model.config.sampling_rate

    def save_audio(self,audio_arr, sampling_rate, output_path="parler_tts_out.wav"):
        sf.write(output_path, audio_arr, sampling_rate)
        return output_path

    def play_audio(self, path):
        wave_obj = sa.WaveObject.from_wave_file(path)
        play_obj = wave_obj.play()
        play_obj.wait_done()