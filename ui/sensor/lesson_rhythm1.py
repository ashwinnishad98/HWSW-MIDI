import time

import board
import neopixel
# import firebase_admin
import pygame
import RPi.GPIO as GPIO
import spidev
# from firebase_admin import credentials, db
from PyQt5.QtCore import QThread, pyqtSignal

# Initialize pygame mixer
pygame.init()
pygame.mixer.init()
drum_sound = pygame.mixer.Sound("kick1.wav")

# Setup SPI for MCP3008
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000
spi.mode = 0

# Setup GPIO for LED
led_pin = board.D18
num_pixels = 6
pixels = neopixel.NeoPixel(led_pin, num_pixels, auto_write=False)


# Define timing for the notes
note_times = [1, 2, 3, 4.5, 5.5, 6.5, 8, 9, 10]
tolerance = 0.5

# Define unique colors for each LED
colors = [
    (255, 0, 0),  # Red
    (0, 255, 0),  # Green
    (100, 0, 255),  # Blue
    (255, 255, 0),  # Yellow
    (0, 255, 255),  # Cyan
    (255, 0, 255),  # Magenta
]
# LED sequence order
led_sequence = [0, 0, 0, 1, 2, 3, 4, 5, 0]

# Setup thresholds and timing for each sensor
threshold = [300] * 6
max_raw_value = 1023
debounce_time = 0.1
last_impact_time = [0] * 6
last_filtered_value = [0] * 6

# Calibrate brightness
to_low = 0.1
to_high = 1.0


def read_channel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data


def map_value(value, from_low, from_high, to_low, to_high):
    """Map value to a different range, applying a square root to increase sensitivity at lower range."""
    range_ratio = (value - from_low) / (from_high - from_low)
    exp_ratio = range_ratio**0.5
    return (exp_ratio * (to_high - to_low)) + to_low


def low_pass_filter(new_value, last_value, alpha=0.2):
    """Apply low-pass filter to smooth the signal."""
    return alpha * new_value + (1 - alpha) * last_value


def play_sequence():
    start_time = time.time()
    for i, note_time in enumerate(note_times):
        while time.time() < start_time + note_time:
            time.sleep(0.01)
        led_index = led_sequence[i]
        pixels[led_index] = colors[led_index]
        pixels.show()
        drum_sound.play()  # Play the drum sound when LED lights up
        time.sleep(0.1)  # LED on duration
        pixels[led_index] = (0, 0, 0)
        pixels.show()


def record_responses():
    start_time = time.time()
    scores = []
    response_times = [[] for _ in range(6)]  # Separate lists for each channel

    while time.time() - start_time < 10:
        current_time = time.time() - start_time
        for channel in range(6):  # Check each channel
            sensor_value = read_channel(channel)
            if sensor_value > 800:  # Threshold for sensor press
                response_times[channel].append(current_time)
                pixels[channel] = colors[channel]  # Turn the specific LED color
                pixels.show()
                drum_sound.play()  # Play the drum sound on sensor press
                time.sleep(0.1)  # LED feedback on sensor press
                pixels[channel] = (0, 0, 0)
                pixels.show()
                while read_channel(channel) > 800:  # Debounce by waiting for release
                    time.sleep(0.01)

    # Check each response time against the expected times
    for note_time in note_times:
        scores.append(
            any(
                abs(note_time - t) <= tolerance
                for times in response_times
                for t in times
            )
        )

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
        scores = record_responses()
        score = sum(scores)
        self.score_signal.emit(f"Your score: {score}/{len(note_times)}")
