# A small app with a keyboard-activatable voice recording which then gets transcribed and saved as text a memo.

# STEPS:
# Step 1: Detect Keyboard Input
# Step 2: Record & Save Voice as a File
import keyboard
import pyaudio
import wave
from pocketsphinx import AudioFile, get_model_path
import os
from datetime import datetime

def record_audio(filename, sample_rate=44100, channels=1, chunk_size=1024):
    try:
        p = pyaudio.PyAudio()

        if channels not in (1, 2):
            raise ValueError("Invalid number of channels. Only 1 (mono) or 2 (stereo) are supported.")

        stream = p.open(format=pyaudio.paInt16,
                        channels=channels,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=chunk_size)

        print("Recording... Press ESC to stop.")

        frames = []

        # Record until ESC is pressed
        while True:
            if keyboard.is_pressed('esc'):
                print("ESC pressed, stopping recording.")
                break
            data = stream.read(chunk_size)
            frames.append(data)

        print("Recording finished.")

        stream.stop_stream()
        stream.close()
        p.terminate()

        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(sample_rate)
            wf.writeframes(b''.join(frames))

    except ValueError as ve:
        print(f"ValueError: {ve}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Step 3: Transcribe the Recording to Text
def transcribe_audio(filename):
    try:
        model_path = 'cmusphinx-en-us-5.'  # Path to your HMM model directory
        dic = 'cmudict-en-us.dict'         # Path to your dictionary file

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"HMM model path not found: {model_path}")
        if not os.path.exists(dic):
            raise FileNotFoundError(f"Dictionary path not found: {dic}")

        # Use PocketSphinx to transcribe audio
        audio_file = AudioFile(audio_file=filename, hmm=model_path, dic=dic)
        
        print("A very inaccurate transcription is being generated...")
        text = ""
        for phrase in audio_file:
            text += phrase.hypothesis() + " "

        print("Transcription:")
        print(text)
    except FileNotFoundError as fnfe:
        print(f"{fnfe}. The transcription library files were not found. The other parts of the program will continue to operate without it.")

# Step 4: Add an automatically generated date string to the filenames
def generate_filename():
    return datetime.now().strftime("recording_%Y%m%d_%H%M%S.wav")

# Step 4.5: Put the program in a loop
def main_loop():
    try:
        is_loop_done = False
        is_text_to_be_displayed = True
        while not is_loop_done:
            if is_text_to_be_displayed:
                print("Waiting for your input (Ctrl+Shift+R to start recording, BACKSPACE to exit):")
            if keyboard.is_pressed("ctrl+shift+r"):
                generated_recording_name = generate_filename()
                record_audio(generated_recording_name, 44100, 1, 1024)
                transcribe_audio(generated_recording_name)
                is_text_to_be_displayed = True
                continue
            if keyboard.is_pressed("backspace"):
                print("Pressed BACKSPACE to stop the program, bye, have a good one!")
                is_loop_done = True

            is_text_to_be_displayed = False    
            keyboard.read_key()

    except KeyboardInterrupt:
        print("Process interrupted. Exiting...")

if __name__ == "__main__":
    main_loop()

# Step 5: Make a UI for it
