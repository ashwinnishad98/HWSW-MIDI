from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QGridLayout, QHBoxLayout, QLabel, QPushButton,
                             QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

from sensor.play_piano import PianoLesson  # Import PianoLesson


class PianoPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.recording = False
        self.initUI()

    def initUI(self):
        self.piano_layout = QVBoxLayout(self)
        self.grid_layout = QGridLayout()

        # Add the grid layout to the piano layout
        self.piano_layout.addLayout(self.grid_layout)

        top_spacer = QSpacerItem(20, 170, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.piano_layout.addItem(top_spacer)

        # Display the piano image
        piano_label = QLabel()
        pixmap = QPixmap("./assets/piano.png").scaled(220, 220, Qt.KeepAspectRatio)
        piano_label.setPixmap(pixmap)
        piano_label.setAlignment(Qt.AlignCenter)
        self.piano_layout.addWidget(piano_label, alignment=Qt.AlignCenter)

        # Add a spacer item to push the button to the bottom
        spacer = QSpacerItem(20, 35, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.piano_layout.addItem(spacer)

        # Button layout for Back and Record buttons
        button_layout = QHBoxLayout()

        # Record button
        self.record_button = QPushButton("Record")
        self.record_button.setFixedWidth(200)
        self.record_button.clicked.connect(self.handle_record_button)
        button_layout.addWidget(self.record_button)

        # Back button
        back_button_piano = QPushButton("Back")
        back_button_piano.setFixedWidth(200)
        back_button_piano.clicked.connect(self.go_back_to_freestyle)
        button_layout.addWidget(back_button_piano)

        button_layout.setAlignment(Qt.AlignCenter)
        self.piano_layout.addLayout(button_layout)

        # Countdown labels
        self.countdown_label = QLabel("")
        self.countdown_label.setAlignment(Qt.AlignCenter)
        self.countdown_label.setStyleSheet("font-size: 36px; color: white;")
        self.piano_layout.addWidget(self.countdown_label, alignment=Qt.AlignCenter)

        self.number_label = QLabel("")
        self.number_label.setAlignment(Qt.AlignCenter)
        self.number_label.setStyleSheet("font-size: 48px; color: white;")
        self.piano_layout.addWidget(self.number_label, alignment=Qt.AlignCenter)

        # Set the layout
        self.setLayout(self.piano_layout)

        # Initialize the piano lesson for playing without recording
        self.piano_lesson = PianoLesson(record=False)
        self.piano_lesson.start()

    def handle_record_button(self):
        if not self.recording:
            self.start_countdown()
        else:
            self.stop_recording()

    def start_countdown(self):
        self.countdown_label.setText("Starting in...")
        self.count = 3
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_countdown)
        self.timer.start(1000)

    def update_countdown(self):
        if self.count > 0:
            self.number_label.setText(str(self.count))
            self.count -= 1
        else:
            self.timer.stop()
            self.countdown_label.setText("")
            self.number_label.setText("")
            self.start_recording()

    def start_recording(self):
        self.recording = True
        self.record_button.setText("Stop Recording")
        self.piano_lesson.terminate()
        self.piano_lesson = PianoLesson(record=True)
        self.piano_lesson.finished.connect(self.recording_finished)
        self.piano_lesson.start()

    def stop_recording(self):
        self.recording = False
        self.record_button.setText("Record")
        self.piano_lesson.terminate()
        self.piano_lesson = PianoLesson(record=False)
        self.piano_lesson.start()

    def recording_finished(self):
        print("Recording finished. Audio saved.")
        self.stop_recording()

    def go_back_to_freestyle(self):
        self.piano_lesson.stop()  # Stop the piano lesson
        self.parent.setCurrentWidget(self.parent)
        self.parent.removeWidget(self)
