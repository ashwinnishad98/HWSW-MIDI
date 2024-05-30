import os
import time
import wave

import numpy as np
from PyQt5.QtCore import QThread

# Recording parameters
sample_rate = 44100


class SaveRecordingThread(QThread):
    def __init__(self, recording, session_folder, instrument):
        super().__init__()
        self.recording = recording
        self.session_folder = session_folder
        self.instrument = instrument

    def run(self):
        # Create a unique file name for the recording
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"{self.instrument}_recording_{timestamp}.wav"
        filepath = os.path.join(self.session_folder, filename)

        wf = wave.open(filepath, "wb")
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(self.recording.astype(np.int16).tobytes())
        wf.close()
        print(f"Recording saved at {filepath}")
