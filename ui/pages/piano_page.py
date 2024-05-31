from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QGridLayout, QHBoxLayout, QLabel, QPushButton,
                             QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

from sensor.play_piano import PianoLesson
from sensor.save_recording_thread import SaveRecordingThread


class PianoPage(QWidget):
    def __init__(self, parent, stacked_widget, session_folder):
        super().__init__(parent)
        self.parent = parent
        self.session_folder = session_folder
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        self.piano_layout = QVBoxLayout(self)
        self.grid_layout = QGridLayout()

        # Add the grid layout to the piano layout
        self.piano_layout.addLayout(self.grid_layout)

        # top_spacer = QSpacerItem(20, 80, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # self.piano_layout.addItem(top_spacer)

        # Display the piano image
        piano_label = QLabel()
        pixmap = QPixmap("./assets/piano.png").scaled(220, 220, Qt.KeepAspectRatio)
        piano_label.setPixmap(pixmap)
        piano_label.setAlignment(Qt.AlignCenter)
        self.piano_layout.addWidget(piano_label, alignment=Qt.AlignCenter)

        # Add a spacer item to push the button to the bottom
        # spacer = QSpacerItem(20, 35, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # self.piano_layout.addItem(spacer)

        # Button layout for Back and Record buttons
        button_layout = QHBoxLayout()

        # Record button
        self.record_button = QPushButton("Record")
        self.record_button.setFixedWidth(200)
        self.record_button.clicked.connect(self.start_recording)
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

    def start_recording(self):
        self.record_button.setDisabled(True)
        self.countdown_label = QLabel("Starting in...")
        self.countdown_label.setAlignment(Qt.AlignCenter)
        self.countdown_label.setStyleSheet("font-size: 36px; color: white;")
        self.piano_layout.addWidget(self.countdown_label, alignment=Qt.AlignCenter)

        self.countdown_value = 3
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_countdown)
        self.timer.start(1000)

    def update_countdown(self):
        if self.countdown_value > 0:
            self.countdown_label.setText(f"{self.countdown_value}")
            self.countdown_value -= 1
        else:
            self.timer.stop()
            self.countdown_label.setText("Recording...")
            self.piano_lesson.stop()
            self.piano_lesson = PianoLesson(record=True)
            self.piano_lesson.recording_signal.connect(self.save_recording)
            self.piano_lesson.finished.connect(self.recording_finished)
            self.piano_lesson.start()

    def save_recording(self, recording):
        self.save_thread = SaveRecordingThread(recording, self.session_folder, "piano")
        self.save_thread.start()

    def recording_finished(self):
        self.countdown_label.setText("Recording finished.")
        QTimer.singleShot(2000, self.reset_ui)  # Show message for 2 seconds

    def reset_ui(self):
        self.countdown_label.deleteLater()
        self.record_button.setDisabled(False)

    def go_back_to_freestyle(self):
        self.piano_lesson.stop()  # Stop the piano lesson
        self.stacked_widget.setCurrentWidget(self.parent)
