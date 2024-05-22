import math
import time

import firebase_admin
import pygame
import RPi.GPIO as GPIO
import spidev
from firebase_admin import credentials, db
from PyQt5.QtCore import QThread, pyqtSignal

# Initialize Firebase
cred = credentials.Certificate("firebasepvt.json")
firebase_admin.initialize_app(
    cred, {"databaseURL": "https://hwsw2-e6856-default-rtdb.firebaseio.com/"}
)

# Initialize pygame mixer
pygame.init()
pygame.mixer.init()
drum_sound = pygame.mixer.Sound("ui/assets/sounds/kick1.wav")

# Setup SPI for MCP3008
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

# Setup GPIO for LED
led_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)

pwm = GPIO.PWM(led_pin, 1000)  # Set PWM frequency to 1000 Hz
pwm.start(0)  # Start PWM with 0% duty cycle

# Define timing for the notes
note_times = [1, 2, 3, 5, 7]
tolerance = 0.5


def update_leaderboard(username, score):
    ref = db.reference("leaderboard")
    user_ref = ref.child(username)
    user_data = user_ref.get()
    if user_data is None:
        user_ref.set({"username": username, "score": score})
    else:
        current_score = user_data["score"]
        if score > current_score:
            user_ref.update({"score": score})


def read_channel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data


def play_sequence():
    start_time = time.time()
    for note_time in note_times:
        while time.time() < start_time + note_time:
            time.sleep(0.01)
        GPIO.output(led_pin, True)
        drum_sound.play()  # Play the drum sound when LED lights up
        time.sleep(0.1)  # LED on duration
        GPIO.output(led_pin, False)


def record_responses():
    start_time = time.time()
    scores = []
    response_times = []

    while time.time() - start_time < 10:
        current_time = time.time() - start_time
        sensor_value = read_channel(0)

        if sensor_value > 800:  # Threshold for sensor press
            response_times.append(current_time)
            GPIO.output(led_pin, True)
            drum_sound.play()  # Play the drum sound on sensor press
            time.sleep(0.1)  # LED feedback on sensor press
            GPIO.output(led_pin, False)
            while read_channel(0) > 800:  # Debounce by waiting for release
                time.sleep(0.01)

    # Check each response time against the expected times
    for note_time in note_times:
        scores.append(any(abs(note_time - t) <= tolerance for t in response_times))

    return scores


class RhythmLesson(QThread):
    progress = pyqtSignal(str)
    sequence_complete = pyqtSignal()
    score_signal = pyqtSignal(str)

    def __init__(self, username):
        super().__init__()
        self.username = username

    def run(self):
        play_sequence()
        self.sequence_complete.emit()
        self.progress.emit(
            "Now your turn! Follow the sequence. Press on the seconds indicated starting in 3 seconds..."
        )
        time.sleep(1)
        self.progress.emit("2 seconds...")
        time.sleep(1)
        self.progress.emit("1 second...")
        time.sleep(1)
        self.progress.emit("Start!")
        scores = record_responses()
        score = sum(scores)
        self.progress.emit(f"Your score: {score}/{len(note_times)}")
        update_leaderboard(self.username, score)
        self.score_signal.emit(f"Your score: {score}/{len(note_times)}")
