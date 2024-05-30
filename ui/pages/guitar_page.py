from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QGridLayout, QHBoxLayout, QLabel, QPushButton,
                             QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

from sensor.play_guitar import GuitarLesson  # Import GuitarLesson


class GuitarPage(QWidget):
    def __init__(self, parent, stacked_widget):
        super().__init__(parent)
        self.parent = parent
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        guitar_layout = QVBoxLayout(self)
        self.grid_layout = QGridLayout()

        # Add the grid layout to the piano layout
        guitar_layout.addLayout(self.grid_layout)

        top_spacer = QSpacerItem(20, 170, QSizePolicy.Minimum, QSizePolicy.Expanding)
        guitar_layout.addItem(top_spacer)

        # Display the piano image
        piano_label = QLabel()
        pixmap = QPixmap("./assets/guitar.png").scaled(180, 180, Qt.KeepAspectRatio)
        piano_label.setPixmap(pixmap)
        piano_label.setAlignment(Qt.AlignCenter)
        guitar_layout.addWidget(piano_label, alignment=Qt.AlignCenter)

        # Add a spacer item to push the button to the bottom
        spacer = QSpacerItem(20, 35, QSizePolicy.Minimum, QSizePolicy.Expanding)
        guitar_layout.addItem(spacer)

        # Start the guitar lesson when the page is displayed
        self.guitar_lesson = GuitarLesson()
        self.guitar_lesson.start()

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
        guitar_layout.addLayout(button_layout)

        # Set the layout
        self.setLayout(guitar_layout)

    def go_back_to_freestyle(self):
        self.guitar_lesson.stop()  # Stop the guitar lesson
        self.stacked_widget.setCurrentWidget(self.parent)
