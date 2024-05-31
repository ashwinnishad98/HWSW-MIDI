from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QGridLayout, QHBoxLayout, QLabel, QPushButton,
                             QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

from sensor.play_guitar import GuitarLesson  # Import GuitarLesson
from sensor.save_recording_thread import SaveRecordingThread


class GuitarPage(QWidget):
    def __init__(self, parent, stacked_widget, session_folder):
        super().__init__(parent)
        self.parent = parent
        self.session_folder = session_folder
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        self.guitar_layout = QVBoxLayout(self)
        self.grid_layout = QGridLayout()

        # Add the grid layout to the guitar layout
        self.guitar_layout.addLayout(self.grid_layout)

        top_spacer = QSpacerItem(20, 80, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.guitar_layout.addItem(top_spacer)

        # Display the guitar image
        guitar_label = QLabel()
        pixmap = QPixmap("./assets/guitar.png").scaled(180, 180, Qt.KeepAspectRatio)
        guitar_label.setPixmap(pixmap)
        guitar_label.setAlignment(Qt.AlignCenter)
        self.guitar_layout.addWidget(guitar_label, alignment=Qt.AlignCenter)
        
        # Countdown labels
        self.countdown_label = QLabel("")
        self.countdown_label.setAlignment(Qt.AlignCenter)
        self.countdown_label.setStyleSheet("font-size: 36px; color: white;")
        self.guitar_layout.addWidget(self.countdown_label, alignment=Qt.AlignCenter)

        self.number_label = QLabel("")
        self.number_label.setAlignment(Qt.AlignCenter)
        self.number_label.setStyleSheet("font-size: 48px; color: white;")
        self.guitar_layout.addWidget(self.number_label, alignment=Qt.AlignCenter)

        # Add a spacer item to push the button to the bottom
        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.guitar_layout.addItem(spacer)

        # Start the guitar lesson when the page is displayed
        self.guitar_lesson = GuitarLesson()
        self.guitar_lesson.start()

        # Button layout for Back and Record buttons
        button_layout = QHBoxLayout()

        # Record button
        self.record_button = QPushButton("Record")
        self.record_button.setFixedWidth(200)
        self.record_button.clicked.connect(self.start_recording)
        button_layout.addWidget(self.record_button)

        # Back button
        back_button_guitar = QPushButton("Back")
        back_button_guitar.setFixedWidth(200)
        back_button_guitar.clicked.connect(self.go_back_to_freestyle)
        button_layout.addWidget(back_button_guitar)

        button_layout.setAlignment(Qt.AlignCenter)
        self.guitar_layout.addLayout(button_layout)
        
        bottom_spacer = QSpacerItem(20, 80, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.guitar_layout.addItem(bottom_spacer)

        # Set the layout
        self.setLayout(self.guitar_layout)

        self.guitar_lesson = GuitarLesson(record=False)
        self.guitar_lesson.start()

    def start_recording(self):
        self.record_button.setDisabled(True)
        self.countdown_label.setText("Starting in...")
        self.countdown_label.setAlignment(Qt.AlignCenter)
        self.countdown_label.setStyleSheet("font-size: 24px; color: white;")
        # self.guitar_layout.addWidget(self.countdown_label, alignment=Qt.AlignCenter)

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
            self.countdown_label.setText("Recording...  You have 10 seconds!")
            self.guitar_lesson.stop()
            self.guitar_lesson = GuitarLesson(record=True)
            self.guitar_lesson.recording_signal.connect(self.save_recording)
            self.guitar_lesson.finished.connect(self.recording_finished)
            self.guitar_lesson.start()

    def save_recording(self, recording):
        self.save_thread = SaveRecordingThread(recording, self.session_folder, "guitar")
        self.save_thread.start()

    def recording_finished(self):
        self.countdown_label.setText("Recording finished.")
        QTimer.singleShot(2000, self.reset_ui)  # Show message for 2 seconds

    def reset_ui(self):
        self.countdown_label.clear()
        self.record_button.setDisabled(False)

    def go_back_to_freestyle(self):
        self.guitar_lesson.stop()  # Stop the guitar lesson
        self.stacked_widget.setCurrentWidget(self.parent)
