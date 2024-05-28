import time
import pygame
import RPi.GPIO as GPIO
import spidev
import board
import neopixel
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
    "./sounds/piano/a.mp3",
    "./sounds/piano/b.mp3",
    "./sounds/piano/c.mp3",
    "./sounds/piano/d.mp3",
    "./sounds/piano/e.mp3",
    "./sounds/piano/f.mp3",
]


class PianoLesson(QThread):
    progress = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.running = True

    def run(self):
        while self.running:
            for channel in range(6):
                sensor_value = self.read_channel(channel)
                if sensor_value > 800:  # Threshold for sensor press
                    self.play_sound(channel)
                    pixels[channel] = colors[channel]  # Turn the specific LED color
                    pixels.show()
                    time.sleep(0.1)  # LED feedback on sensor press
                    pixels[channel] = (0, 0, 0)
                    pixels.show()
                    while (
                        self.read_channel(channel) > 800
                    ):  # Debounce by waiting for release
                        time.sleep(0.01)

    def read_channel(self, channel):
        adc = spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data

    def play_sound(self, channel):
        sound = pygame.mixer.Sound(note_files[channel])
        sound.play()

    def stop(self):
        self.running = False
        self.quit()
        self.wait()
