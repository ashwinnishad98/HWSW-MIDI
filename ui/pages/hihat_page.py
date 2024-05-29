from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QGridLayout, QHBoxLayout, QLabel, QPushButton,
                             QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

from sensor.play_hihat import HiHatLesson  # Import HiHatLesson


class HiHatPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        hihat_layout = QVBoxLayout(self)
        self.grid_layout = QGridLayout()

        # Add the grid layout to the piano layout
        hihat_layout.addLayout(self.grid_layout)

        top_spacer = QSpacerItem(20, 170, QSizePolicy.Minimum, QSizePolicy.Expanding)
        hihat_layout.addItem(top_spacer)

        # Display the piano image
        piano_label = QLabel()
        pixmap = QPixmap("./assets/hi-hat.png").scaled(220, 220, Qt.KeepAspectRatio)
        piano_label.setPixmap(pixmap)
        piano_label.setAlignment(Qt.AlignCenter)
        hihat_layout.addWidget(piano_label, alignment=Qt.AlignCenter)

        # Add a spacer item to push the button to the bottom
        spacer = QSpacerItem(20, 35, QSizePolicy.Minimum, QSizePolicy.Expanding)
        hihat_layout.addItem(spacer)

        # Start the hihat lesson when the page is displayed
        self.hihat_lesson = HiHatLesson()
        self.hihat_lesson.start()

        # Button layout for Back and Record buttons
        button_layout = QHBoxLayout()

        # Record button
        record_button = QPushButton("Record")
        record_button.setFixedWidth(200)
        record_button.clicked.connect(
            self.go_back_to_freestyle
        )  # TODO: update functionality later
        button_layout.addWidget(record_button)

        # Back button
        back_button_piano = QPushButton("Back")
        back_button_piano.setFixedWidth(200)
        back_button_piano.clicked.connect(self.go_back_to_freestyle)
        button_layout.addWidget(back_button_piano)

        button_layout.setAlignment(Qt.AlignCenter)
        hihat_layout.addLayout(button_layout)

        # Set the layout
        self.setLayout(hihat_layout)

    def go_back_to_freestyle(self):
        self.hihat_lesson.stop()  # Stop the hihat lesson
        self.parent.setCurrentWidget(self.parent.parent())
        self.parent.removeWidget(self)
