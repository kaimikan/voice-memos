# A small app with a keyboard-activatable voice recording which then gets transcribed and saved as text a memo.

# STEPS:
# Step 1: Detect Keyboard Input
# Step 2: Record & Save Voice as a File
import keyboard
import pyaudio
import wave

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

# Usage example with hotkey
keyboard.add_hotkey('ctrl+shift+r', record_audio, args=('output.wav', 44100, 1, 1024))

print("Press Ctrl+Shift+R to start recording. Press ESC to stop.")
keyboard.wait('esc')

# Step 3: Transcribe the Recording to Text
# Step 4: Add an automatically generated date string to the filenames
# Step 5: Make a UI for it
