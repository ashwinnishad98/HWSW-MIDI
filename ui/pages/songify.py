import os
import wave

import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal


class Songify(QThread):
    finished = pyqtSignal()

    def __init__(self, session_folder):
        super().__init__()
        self.session_folder = session_folder

    def run(self):
        wav_files = [f for f in os.listdir(self.session_folder) if f.endswith(".wav")]
        if not wav_files:
            self.finished.emit()
            return

        combined_audio = None
        for wav_file in wav_files:
            filepath = os.path.join(self.session_folder, wav_file)
            with wave.open(filepath, "rb") as wf:
                audio = wf.readframes(wf.getnframes())
                audio = np.frombuffer(audio, dtype=np.int16)
                if combined_audio is None:
                    combined_audio = audio
                else:
                    combined_audio = np.add(combined_audio, audio, casting="safe")

        combined_audio = np.clip(combined_audio, -32768, 32767)

        output_filepath = os.path.join(self.session_folder, "final.wav")
        with wave.open(output_filepath, "wb") as wf:
            wf.setnchannels(2)
            wf.setsampwidth(2)
            wf.setframerate(44100)
            wf.writeframes(combined_audio.astype(np.int16).tobytes())

        self.finished.emit()
