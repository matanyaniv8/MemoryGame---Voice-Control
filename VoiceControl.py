from vosk import Model, KaldiRecognizer
import sounddevice as sd
import json
import queue
from threading import Thread
import pygame


def text_to_number(text):
    number_words = {
        "one": 1, "two": 2, "three": 3, "four": 4, "for": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
        "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fortheen": 14,
        "fifteen": 15, "sixteen": 16
    }
    return number_words.get(text.lower(), -1)


class VoiceControl:
    VOICE_RECOGNIZE_EVENT_TYPE = pygame.USEREVENT + 1

    def __init__(self, model_path="./voice-rec/vosk-model-small-en-us-0.15"):
        self.process_thread = None
        self.stream = None
        # Using a thread-safe queue for commands to ensure safe cross-thread operations
        self.commands_queue = queue.Queue()
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, 16000)
        self.running = False  # Flag to control the background processing thread
        self.commands = []

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status)
        data_bytes = bytes(indata)
        if self.recognizer.AcceptWaveform(data_bytes):
            result = json.loads(self.recognizer.Result())
            command = result.get('text', '').lower()
            if command:
                # Use put_nowait to add to the queue without blocking
                self.commands_queue.put_nowait(command)

    def start_listening(self):
        self.running = True
        self.stream = sd.RawInputStream(samplerate=16000, channels=1, dtype='int16', callback=self.audio_callback)
        self.stream.start()
        # Start a background thread to process commands
        self.process_thread = Thread(target=self.process_commands)
        # self.process_thread.daemon = True
        self.process_thread.start()

    def stop_listening(self):
        self.running = False
        self.stream.stop()
        self.stream.close()
        self.process_thread.join()  # Ensure the processing thread has finished

    def process_commands(self):
        while self.running or not self.commands_queue.empty():
            try:
                # Use get with timeout to avoid blocking indefinitely
                command = self.commands_queue.get(timeout=1)
                self.handle_command(command)
            except queue.Empty:
                pass  # Timeout reached, loop back to check running status

    def handle_command(self, command):
        list_of_commands = command.split(' ')
        for command in list_of_commands:
            number = text_to_number(command)
            # Process the number or command as needed
            if number != -1:
                pygame.event.post(pygame.event.Event(VoiceControl.VOICE_RECOGNIZE_EVENT_TYPE, data=number))


