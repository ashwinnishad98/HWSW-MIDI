import time
import wave

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
    "./sounds/piano/C.wav",
    "./sounds/piano/D.wav",
    "./sounds/piano/E.wav",
    "./sounds/piano/F.wav",
    "./sounds/piano/G.wav",
    "./sounds/piano/A.wav",
]

# Recording parameters
sample_rate = 44100
recording_duration = 10  # seconds


def read_channel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data


class PianoLesson(QThread):
    finished = pyqtSignal()
    recording_signal = pyqtSignal(np.ndarray)

    def __init__(self, record=False):
        super().__init__()
        self.record = record
        self.running = True

    def run(self):
        if self.record:
            self.record_piano()
        else:
            self.play_piano()

    def play_piano(self):
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

    def record_piano(self):
        print("Recording started.")
        recording = np.zeros((recording_duration * sample_rate, 2))  # Stereo recording

        start_time = time.time()
        for i in range(recording_duration * sample_rate):
            if not self.running:
                break
            if time.time() - start_time >= recording_duration:
                break

            for j in range(num_pixels):
                sensor_value = read_channel(j)
                if sensor_value > 800:  # Threshold for sensor press
                    pygame.mixer.Sound(note_files[j]).play()  # Play corresponding note
                    pixels[j] = colors[j]
                    pixels.show()
                    time.sleep(0.1)
                    pixels[j] = (0, 0, 0)
                    pixels.show()

                    # Add audio to recording
                    recording[i] = np.array([sensor_value, sensor_value])

        self.recording_signal.emit(recording)
        self.finished.emit()
        print("Recording finished.")

    def stop(self):
        self.running = False
        self.quit()
        self.wait()


class SaveRecordingThread(QThread):
    def __init__(self, recording):
        super().__init__()
        self.recording = recording

    def run(self):
        wf = wave.open("piano_recording.wav", "wb")
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(self.recording.astype(np.int16).tobytes())
        wf.close()
        print("Recording saved as piano_recording.wav.")
