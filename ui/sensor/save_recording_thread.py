import wave

import numpy as np
from PyQt5.QtCore import QThread

# Recording parameters
sample_rate = 44100


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
