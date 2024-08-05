import schedule
import time
import pygame

REMIND_ME_EVERY_X_MINUTES = 1

def play_audio_message():
    pygame.mixer.init()
    pygame.mixer.music.load('reminder.wav')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(1)
    print("Played the reminder.")

# Schedule the task
schedule.every(REMIND_ME_EVERY_X_MINUTES).minutes.do(play_audio_message)

print(f"Reminder started and will play every {REMIND_ME_EVERY_X_MINUTES} minute(s). Press Ctrl+C to exit.")
play_audio_message();

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)