import time

import board
import neopixel
import numpy as np
import pygame
import spidev
from PyQt5.QtCore import QThread, pyqtSignal

# Initialize pygame mixer
pygame.init()
pygame.mixer.init()

# Setup SPI for MCP3008
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000
spi.mode = 0

# Setup GPIO for LED
led_pin = board.D18
num_pixels = 6
pixels = neopixel.NeoPixel(led_pin, num_pixels, auto_write=False)

# Define unique colors for each LED
colors = [
    (255, 0, 0),  # Red
    (0, 255, 0),  # Green
    (100, 0, 255),  # Blue
    (255, 255, 0),  # Yellow
    (0, 255, 255),  # Cyan
    (255, 0, 255),  # Magenta
]

note_files = [
    "./sounds/kick/1.wav",
    "./sounds/kick/2.wav",
    "./sounds/kick/3.wav",
    "./sounds/kick/4.wav",
    "./sounds/kick/5.wav",
    "./sounds/kick/6.wav",
]

# Recording parameters
sample_rate = 44100
recording_duration = 10  # seconds


def read_channel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data


class KickLesson(QThread):
    finished = pyqtSignal()
    recording_signal = pyqtSignal(np.ndarray)

    def __init__(self, record=False):
        super().__init__()
        self.record = record
        self.running = True

    def run(self):
        if self.record:
            self.record_kick()
        else:
            self.play_kick()

    def play_kick(self):
        while self.running:
            for j in range(num_pixels):
                sensor_value = read_channel(j)
                if sensor_value > 800:  # Threshold for sensor press
                    pygame.mixer.Sound(note_files[j]).play()
                    pixels[j] = colors[j]
                    pixels.show()
                    time.sleep(0.1)
                    pixels[j] = (0, 0, 0)
                    pixels.show()
                    time.sleep(0.1)  # Debounce time

    def record_kick(self):
        print("Recording started.")
        recording = np.zeros((recording_duration * sample_rate, 2))  # Stereo recording

        start_time = time.time()
        current_index = 0

        while time.time() - start_time < recording_duration:
            if not self.running:
                break

            for j in range(num_pixels):
                sensor_value = read_channel(j)
                if sensor_value > 800:  # Threshold for sensor press
                    sound = pygame.mixer.Sound(note_files[j])
                    sound.play()
                    pixels[j] = colors[j]
                    pixels.show()
                    time.sleep(0.1)
                    pixels[j] = (0, 0, 0)
                    pixels.show()

                    # Capture the played sound
                    sound_array = pygame.sndarray.array(sound)
                    num_samples = len(sound_array)

                    if current_index + num_samples < len(recording):
                        recording[current_index : current_index + num_samples] = (
                            sound_array[:num_samples]
                        )
                    else:
                        break

                    current_index += num_samples

        print("Recording captured.")
        self.recording_signal.emit(recording)
        self.finished.emit()

    def stop(self):
        self.running = False
        self.quit()
        self.wait()
