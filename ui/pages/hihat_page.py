from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)

from sensor.play_hihat import HiHatLesson  # Import HiHatLesson
from sensor.save_recording_thread import SaveRecordingThread


class HiHatPage(QWidget):
    def __init__(self, parent, stacked_widget, session_folder):
        super().__init__(parent)
        self.parent = parent
        self.session_folder = session_folder
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        self.hihat_layout = QVBoxLayout(self)
        self.grid_layout = QGridLayout()

        # Add the grid layout to the hihat layout
        self.hihat_layout.addLayout(self.grid_layout)

        top_spacer = QSpacerItem(20, 170, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.hihat_layout.addItem(top_spacer)

        # Display the hihat image
        hihat_label = QLabel()
        pixmap = QPixmap("./assets/hi-hat.png").scaled(220, 220, Qt.KeepAspectRatio)
        hihat_label.setPixmap(pixmap)
        hihat_label.setAlignment(Qt.AlignCenter)
        self.hihat_layout.addWidget(hihat_label, alignment=Qt.AlignCenter)

        # Add a spacer item to push the button to the bottom
        spacer = QSpacerItem(20, 35, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.hihat_layout.addItem(spacer)

        # Start the hihat lesson when the page is displayed
        self.hihat_lesson = HiHatLesson()
        self.hihat_lesson.start()

        # Button layout for Back and Record buttons
        button_layout = QHBoxLayout()

        # Record button
        record_button = QPushButton("Record")
        record_button.setFixedWidth(200)
        record_button.clicked.connect(self.start_recording)
        button_layout.addWidget(record_button)

        # Back button
        back_button_hihat = QPushButton("Back")
        back_button_hihat.setFixedWidth(200)
        back_button_hihat.clicked.connect(self.go_back_to_freestyle)
        button_layout.addWidget(back_button_hihat)

        button_layout.setAlignment(Qt.AlignCenter)
        self.hihat_layout.addLayout(button_layout)

        # Countdown labels
        self.countdown_label = QLabel("")
        self.countdown_label.setAlignment(Qt.AlignCenter)
        self.countdown_label.setStyleSheet("font-size: 36px; color: white;")
        self.hihat_layout.addWidget(self.countdown_label, alignment=Qt.AlignCenter)

        self.number_label = QLabel("")
        self.number_label.setAlignment(Qt.AlignCenter)
        self.number_label.setStyleSheet("font-size: 48px; color: white;")
        self.hihat_layout.addWidget(self.number_label, alignment=Qt.AlignCenter)

        # Set the layout
        self.setLayout(self.hihat_layout)

        # Initialize the hihat lesson for playing without recording
        self.hihat_lesson = HiHatLesson(record=False)
        self.hihat_lesson.start()

    def start_recording(self):
        self.record_button.setDisabled(True)
        self.countdown_label = QLabel("Starting in...")
        self.countdown_label.setAlignment(Qt.AlignCenter)
        self.countdown_label.setStyleSheet("font-size: 36px; color: white;")
        self.hihat_layout.addWidget(self.countdown_label, alignment=Qt.AlignCenter)

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
            self.hihat_lesson = HiHatLesson(record=True)
            self.hihat_lesson.recording_signal.connect(self.save_recording)
            self.hihat_lesson.finished.connect(self.recording_finished)
            self.hihat_lesson.start()

    def save_recording(self, recording):
        self.save_thread = SaveRecordingThread(recording, self.session_folder, "guitar")
        self.save_thread.start()

    def recording_finished(self):
        self.countdown_label.setText("Recording finished.")
        QTimer.singleShot(2000, self.reset_ui)  # Show message for 2 seconds

    def reset_ui(self):
        self.countdown_label.deleteLater()
        self.record_button.setDisabled(False)

    def go_back_to_freestyle(self):
        self.hihat_lesson.stop()  # Stop the hihat lesson
        self.stacked_widget.setCurrentWidget(self.parent)
