from vosk import Model, KaldiRecognizer
import sounddevice as sd
import json


class VoiceControl:
    def __init__(self, model_path="./voice-rec/vosk-model-small-en-us-0.15"):
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, 16000)
        self.commands_queue = []
        self.number_words = {
            "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
            "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
            "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16
        }

    def audio_callback(self, indata, frames, time, status):
        # Direct conversion of _cffi_backend.buffer to bytes
        data_bytes = bytes(indata)
        if self.recognizer.AcceptWaveform(data_bytes):
            result = json.loads(self.recognizer.Result())
            command = result.get('text', '').lower()
            if command:
                self.commands_queue.append(command)

    def start_listening(self):
        self.stream = sd.RawInputStream(samplerate=16000, channels=1, dtype='int16', callback=self.audio_callback)
        self.stream.start()

    def stop_listening(self):
        self.stream.stop()
        self.stream.close()

    def process_commands(self):
        if self.commands_queue:
            command = self.commands_queue.pop(0)
            number = self.text_to_number(command)
            return number
        return None

    def text_to_number(self, text):
        num = -1

        if text.lower() in self.number_words.keys():
            num = self.number_words[text.lower()]
        return num
